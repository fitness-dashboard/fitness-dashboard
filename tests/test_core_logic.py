import unittest

import pandas as pd

from gymrun_calculations import (
    build_gym_max_rm,
    build_gym_volume
)
from gymrun_config import GYM_EXERCISES
from body import build_body_dataframe
from nutrition import (
    build_nutrition_dataframe,
    calculate_macro_targets,
    get_nutrition_phase
)
from training import (
    filter_training_block,
    get_new_prs,
    get_training_block
)


class NutritionTests(unittest.TestCase):

    def test_get_nutrition_phase_returns_matching_phase(self):

        phase = get_nutrition_phase(
            "2026-07-20"
        )

        self.assertEqual(
            phase["phase"],
            4
        )

    def test_calculate_macro_targets_includes_training_calories(self):

        targets = calculate_macro_targets(
            "2026-07-20",
            80,
            training_calories=300
        )

        self.assertEqual(
            targets,
            {
                "calories": 2200,
                "protein": 160,
                "fat": 56,
                "carbs": 264
            }
        )

    def test_calculate_macro_targets_returns_none_outside_phase(self):

        targets = calculate_macro_targets(
            "2031-01-01",
            80
        )

        self.assertIsNone(
            targets
        )

    def test_build_nutrition_dataframe_calculates_targets(self):

        df_gesamt = pd.DataFrame(
            {
                "Only Date": pd.to_datetime(
                    ["2026-07-20"]
                ),
                "Weight (kg)": [80],
                "Körperfettanteil kg": [20],
                "Muscle Mass (kg)": [60],
                "Kalorien aus Training": [300],
                "Kalorien": [2200],
                "Eiweiß (g)": [160],
                "Fett (g)": [56],
                "Kohlenhydrate (g)": [264]
            }
        )

        result = build_nutrition_dataframe(
            df_gesamt
        )

        self.assertEqual(
            result.loc[0, "Nutrition Phase"],
            "Phase 4"
        )

        self.assertEqual(
            result.loc[0, "Calories Target"],
            2200
        )

        self.assertEqual(
            result.loc[0, "Protein %"],
            100
        )


class BodyTests(unittest.TestCase):

    def test_build_body_dataframe_creates_rolling_average(self):

        df_gesamt = pd.DataFrame(
            {
                "Only Date": pd.to_datetime(
                    [
                        "2026-07-19",
                        "2026-07-20"
                    ]
                ),
                "Weight (kg)": [80, 78],
                "Weight (kg) 7 Tage": [80, 79],
                "Body Fat (%)": [25, 24],
                "Körperfettanteil kg": [20, 18.72],
                "Muscle Mass (kg)": [60, 61],
                "BMI": [25, 24.6],
                "BMR (kcal)": [1800, 1810],
                "Visc Fat": [10, 9],
                "Body Water (%)": [50, 51],
                "Bone Mass (kg)": [3, 3.1],
                "Metab Age": [50, 49],
                "Muscle mass - right arm": [3, 3.1],
                "Muscle mass - left arm": [3, 3.1],
                "Muscle mass - trunk": [30, 30.5],
                "Muscle mass - right leg": [10, 10.2],
                "Muscle mass - left leg": [10, 10.2],
                "Body fat (%) - right arm": [20, 19],
                "Body fat (%) - left arm": [20, 19],
                "Body fat (%) - trunk": [30, 29],
                "Body fat (%) - right leg": [25, 24],
                "Body fat (%) - left leg": [25, 24]
            }
        )

        result = build_body_dataframe(
            df_gesamt
        )

        self.assertEqual(
            result.loc[1, "Day"],
            2
        )

        self.assertEqual(
            result.loc[1, "Weight"],
            78
        )

        self.assertEqual(
            result.loc[1, "Body Fat % 7 Days"],
            24.5
        )


class GymRunCalculationsTests(unittest.TestCase):

    def setUp(self):

        self.df_gymrun = pd.DataFrame(
            {
                "Date": pd.to_datetime(
                    [
                        "2026-06-10",
                        "2026-06-10",
                        "2026-06-10",
                        "2026-06-11"
                    ]
                ),
                "Exercise": [
                    "Bankdrücken",
                    "Bankdrücken",
                    "Kreuzheben",
                    "Bankdrücken"
                ],
                "RM Brzycki": [
                    100,
                    105,
                    140,
                    110
                ],
                "Volume": [
                    800,
                    850,
                    1200,
                    900
                ]
            }
        )

    def test_build_gym_max_rm_uses_daily_maximum(self):

        result = build_gym_max_rm(
            self.df_gymrun
        )

        first_day = result.loc[
            result["Date"] == pd.Timestamp("2026-06-10")
        ].iloc[0]

        self.assertEqual(
            first_day["Bankdrücken"],
            105
        )

        self.assertEqual(
            first_day["Kreuzheben"],
            140
        )

    def test_build_gym_volume_sums_daily_volume(self):

        result = build_gym_volume(
            self.df_gymrun
        )

        first_day = result.loc[
            result["Date"] == pd.Timestamp("2026-06-10")
        ].iloc[0]

        self.assertEqual(
            first_day["Bankdrücken"],
            1650
        )


class TrainingTests(unittest.TestCase):

    def setUp(self):

        self.df_gym_max_rm = pd.DataFrame(
            {
                "Date": pd.to_datetime(
                    [
                        "2025-06-20",
                        "2025-06-21",
                        "2025-06-28"
                    ]
                )
            }
        )

        for exercise in GYM_EXERCISES:

            self.df_gym_max_rm[exercise] = pd.NA

        self.df_gym_max_rm[
            "Flachbankdrücken Langhantel"
        ] = [
            90,
            100,
            105
        ]

    def test_get_training_block_returns_matching_block(self):

        block = get_training_block(
            "2026-06-10"
        )

        self.assertEqual(
            block["block"],
            2
        )

    def test_filter_training_block_returns_only_matching_dates(self):

        result = filter_training_block(
            self.df_gym_max_rm,
            block_number=1
        )

        self.assertEqual(
            len(result),
            2
        )

        self.assertTrue(
            (result["Date"] >= pd.Timestamp("2025-06-21")).all()
        )

    def test_get_new_prs_returns_improvement_in_training_block(self):

        result = get_new_prs(
            self.df_gym_max_rm,
            block_number=1,
            format_date=False
        )

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result.loc[0, "Exercise"],
            "Flachbankdrücken Langhantel"
        )

        self.assertEqual(
            result.loc[0, "Δ RM"],
            5
        )


if __name__ == "__main__":

    unittest.main()
