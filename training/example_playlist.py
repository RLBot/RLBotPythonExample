import hello_world_training
import rlbottraining.common_exercises.bronze_goalie as bronze_goalie
import rlbottraining.common_exercises.rl_custom_training_import.rl_importer as rl_importer

def make_default_playlist():
    exercises = (
        # hello_world_training.make_default_playlist() +
        # bronze_goalie.make_default_playlist()
        rl_importer.make_default_playlist()[:3]
    )
    for exercise in exercises:
        exercise.match_config = hello_world_training.make_match_config_with_my_bot()

    return exercises
