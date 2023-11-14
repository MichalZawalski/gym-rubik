from gym.envs.registration import register

from gym_rubik.envs.rubik_env import RubikEnv, GoalRubikEnv

register(
    id='RubikEnv-v0',
    entry_point='gym_rubik.envs:RubikEnv'
)
