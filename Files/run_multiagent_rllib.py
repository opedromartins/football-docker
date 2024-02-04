# coding=utf-8
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A simple example of setting up a multi-agent version of GFootball with rllib.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tempfile
import argparse
import gfootball.env as football_env
import gym
import ray
from ray import tune
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.tune.registry import register_env

parser = argparse.ArgumentParser()
parser.add_argument('--num-agents', type=int, default=3)
parser.add_argument('--num-policies', type=int, default=3)
parser.add_argument('--num-iters', type=int, default=100000)
parser.add_argument('--simple', action='store_true')

class RllibGFootball(MultiAgentEnv):
    def __init__(self, num_agents):
        self.env = football_env.create_environment(
            env_name='test_example_multiagent', stacked=False,
            logdir=os.path.join(tempfile.gettempdir(), 'rllib_test'),
            write_goal_dumps=False, write_full_episode_dumps=False, render=True,
            dump_frequency=0,
            number_of_left_players_agent_controls=num_agents,
            channel_dimensions=(42, 42))
        self.action_space = gym.spaces.Discrete(self.env.action_space.nvec[1])
        self.observation_space = gym.spaces.Box(
            low=self.env.observation_space.low[0],
            high=self.env.observation_space.high[0],
            dtype=self.env.observation_space.dtype)
        self.num_agents = num_agents

    def reset(self):
        original_obs = self.env.reset()
        obs = {}
        for x in range(self.num_agents):
            obs['agent_%d' % x] = original_obs[x] if self.num_agents > 1 else original_obs
        return obs

    def step(self, action_dict):
        actions = [action for action in action_dict.values()]
        o, r, d, i = self.env.step(actions)
        rewards = {}
        obs = {}
        infos = {}
        for pos, key in enumerate(sorted(action_dict.keys())):
            infos[key] = i
            rewards[key] = r[pos] if self.num_agents > 1 else r
            obs[key] = o[pos] if self.num_agents > 1 else o
        dones = {'__all__': d}
        return obs, rewards, dones, infos

if __name__ == '__main__':
    args = parser.parse_args()
    ray.init(num_gpus=1, ignore_reinit_error=True)

    register_env('gfootball', lambda _: RllibGFootball(args.num_agents))
    single_env = RllibGFootball(args.num_agents)
    obs_space = single_env.observation_space
    act_space = single_env.action_space

    def gen_policy(_):
        return (None, obs_space, act_space, {})

    policies = {
        'policy_{}'.format(i): gen_policy(i) for i in range(args.num_policies)
    }
    policy_ids = list(policies.keys())

    tune.run(
        'PPO',
        stop={'training_iteration': args.num_iters},
        checkpoint_freq=50,
        config={
            'env': 'gfootball',
            'lambda': 0.95,
            'kl_coeff': 0.2,
            'clip_rewards': False,
            'vf_clip_param': 10.0,
            'entropy_coeff': 0.01,
            'train_batch_size': 2000,
            'rollout_fragment_length': 100,
            'sgd_minibatch_size': 500,
            'num_sgd_iter': 10,
            'num_workers': 10,
            'num_envs_per_worker': 1,
            'batch_mode': 'truncate_episodes',
            'observation_filter': 'NoFilter',
            'vf_share_layers': True,
            'num_gpus': 1,
            'lr': 2.5e-4,
            'log_level': 'DEBUG',
            'simple_optimizer': args.simple,
            'multiagent': {
                'policies': policies,
                'policy_mapping_fn': lambda agent_id: policy_ids[int(agent_id.split('_')[-1])],
            },
        },
    )