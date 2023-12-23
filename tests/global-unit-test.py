import gc
import pandas as pd
from chefboost import Chefboost as cb
from chefboost.commons.logger import Logger

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

logger = Logger(module="tests/global-unit-test.py")

# ----------------------------------------------

parallelism_cases = [True]
# parallelism_cases = [False]
# parallelism_cases = [False, True]

if __name__ == "__main__":

    for enableParallelism in parallelism_cases:

        logger.info("*************************")
        logger.info(f"enableParallelism is set to {enableParallelism}")
        logger.info("*************************")

        logger.info("no config passed")
        df = pd.read_csv("dataset/golf.txt")
        model = cb.fit(df)

        gc.collect()

        logger.info("-------------------------")

        logger.info("Validation set case")

        df = pd.read_csv("dataset/golf.txt")
        validation_df = pd.read_csv("dataset/golf.txt")
        config = {"algorithm": "ID3", "enableParallelism": enableParallelism}
        model = cb.fit(df, config, validation_df=validation_df)

        gc.collect()

        logger.info("-------------------------")

        logger.info("Feature importance")
        # decision_rules = model["trees"][0].__dict__["__name__"]+".py"
        decision_rules = model["trees"][0].__dict__["__spec__"].origin
        logger.info(cb.feature_importance(decision_rules))

        logger.info("-------------------------")

        logger.info("ID3 for nominal features and nominal target:")
        df = pd.read_csv("dataset/golf.txt")

        config = {"algorithm": "ID3", "enableParallelism": enableParallelism}
        model = cb.fit(df, config)

        validation_df = pd.read_csv("dataset/golf.txt")

        logger.info("External validation")
        cb.evaluate(model, validation_df)

        cb.save_model(model)
        logger.info("built model is saved to model.pkl")

        restored_model = cb.load_model("model.pkl")
        logger.info("built model is restored from model.pkl")

        instance = ["Sunny", "Hot", "High", "Weak"]
        prediction = cb.predict(restored_model, instance)

        logger.info(f"prediction for {instance} is {prediction}")

        gc.collect()

        logger.info("-------------------------")

        logger.info("ID3 for nominal/numeric features and nominal target:")
        config = {"algorithm": "ID3", "enableParallelism": enableParallelism}
        model = cb.fit(pd.read_csv("dataset/golf2.txt"), config)

        instance = ["Sunny", 85, 85, "Weak"]
        prediction = cb.predict(model, instance)
        logger.info(f"prediction for {instance} is {prediction}")

        gc.collect()

        logger.info("-------------------------")

        logger.info("C4.5 for nominal/numeric features and nominal target:")
        config = {"algorithm": "C4.5", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf2.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("CART for nominal/numeric features and nominal target:")
        config = {"algorithm": "CART", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf2.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("CHAID for nominal features and nominal target:")
        config = {"algorithm": "CHAID", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("CHAID for nominal/numeric features and nominal target:")
        config = {"algorithm": "CHAID", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf2.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("regression tree for nominal features, numeric target")
        config = {"algorithm": "Regression", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf3.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("regression tree for nominal/numeric features, numeric target")
        config = {"algorithm": "Regression", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf4.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info(
            "algorithm must be regression tree for numetic target. set any other algorithm."
        )
        config = {"algorithm": "ID3", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/golf4.txt"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("ID3 for nominal features and target (large data set)")
        config = {"algorithm": "ID3", "enableParallelism": enableParallelism}
        model = cb.fit(pd.read_csv("dataset/car.data"), config)

        instance = ["vhigh", "vhigh", 2, "2", "small", "low"]
        prediction = cb.predict(model, instance)
        logger.info(prediction)

        instance = ["high", "high", "4", "more", "big", "high"]
        prediction = cb.predict(model, instance)
        logger.info(prediction)

        gc.collect()

        logger.info("-------------------------")

        logger.info("C4.5 for nominal features and target (large data set)")
        config = {"algorithm": "C4.5", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/car.data"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("CART for nominal features and target (large data set)")
        config = {"algorithm": "CART", "enableParallelism": enableParallelism}
        cb.fit(pd.read_csv("dataset/car.data"), config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("CHAID for nominal features and target (large data set)")
        config = {"algorithm": "CHAID", "enableParallelism": enableParallelism}
        df = pd.read_csv("dataset/car.data")
        cb.fit(df, config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("Iris with regular decision tree")
        config = {"algorithm": "ID3"}
        df = pd.read_csv(
            "dataset/iris.data",
            names=["Sepal length", "Sepal width", "Petal length", "Petal width", "Decision"],
        )
        model = cb.fit(df, config)

        gc.collect()

        logger.info("-------------------------")

        logger.info("Adaboost")
        config = {
            "algorithm": "ID3",
            "enableAdaboost": True,
            "num_of_weak_classifier": 10,
            "enableParallelism": False,
        }
        df = pd.read_csv("dataset/adaboost.txt")
        validation_df = df.copy()

        model = cb.fit(df, config, validation_df=validation_df)

        instance = [4, 3.5]

        gc.collect()

        logger.info("-------------------------")

        logger.info("Regular GBM")
        config = {
            "algorithm": "CART",
            "enableGBM": True,
            "epochs": 10,
            "learning_rate": 1,
            "enableParallelism": enableParallelism,
        }
        df = pd.read_csv("dataset/golf4.txt")
        validation_df = pd.read_csv("dataset/golf4.txt")
        model = cb.fit(df, config, validation_df=validation_df)

        instance = ["Sunny", 85, 85, "Weak"]
        prediction = cb.predict(model, instance)
        logger.info(f"prediction for {instance} is {prediction}")

        gc.collect()

        logger.info("-------------------------")

        logger.info("GBM for classification")
        config = {
            "algorithm": "ID3",
            "enableGBM": True,
            "epochs": 10,
            "learning_rate": 1,
            "enableParallelism": enableParallelism,
        }

        df = pd.read_csv(
            "dataset/iris.data",
            names=["Sepal length", "Sepal width", "Petal length", "Petal width", "Decision"],
        )
        validation_df = df.copy()

        model = cb.fit(df, config, validation_df=validation_df)

        instance = [7.0, 3.2, 4.7, 1.4]
        prediction = cb.predict(model, instance)
        logger.info(f"prediction for {instance} is {prediction}")

        gc.collect()

        logger.info("-------------------------")

        logger.info("Random forest")
        config = {
            "algorithm": "ID3",
            "enableRandomForest": True,
            "num_of_trees": 3,
            "enableParallelism": enableParallelism,
        }
        df = pd.read_csv("dataset/car.data")
        validation_df = pd.read_csv("dataset/car.data")
        model = cb.fit(
            pd.read_csv("dataset/car.data"),
            config
            # , validation_df = validation_df
        )

        logger.info("Feature importance of random forest")
        decision_rules = []
        for tree in model["trees"]:

            decision_rule = tree.__dict__["__spec__"].origin
            decision_rules.append(decision_rule)

        df = cb.feature_importance(decision_rules)
        logger.info(df)

        instance = ["vhigh", "vhigh", 2, "2", "small", "low"]

        prediction = cb.predict(model, instance)
        logger.info(f"prediction for {instance} is {prediction}")

        instance = ["high", "high", 4, "more", "big", "high"]

        prediction = cb.predict(model, instance)
        logger.info(f"prediction for {instance} is {prediction}")

        gc.collect()

        logger.info("-------------------------")

        logger.info("Random forest for regression")

        config = {
            "algorithm": "ID3",
            "enableRandomForest": True,
            "num_of_trees": 5,
            "enableMultitasking": False,
            "enableParallelism": enableParallelism,
        }

        df = pd.read_csv("dataset/car_reg.data")
        model = cb.fit(pd.read_csv("dataset/car_reg.data"), config)

        validation_df = pd.read_csv("dataset/car_reg.data")
        cb.evaluate(model, validation_df)

        instance = ["high", "high", 4, "more", "big", "high"]
        prediction = cb.predict(model, instance)
        logger.info(f"prediction for {instance} is {prediction}")

        gc.collect()

        logger.info("-------------------------")

        logger.info("Is there any none predictions?")
        config = {"algorithm": "C4.5", "enableParallelism": enableParallelism}
        model = cb.fit(pd.read_csv("dataset/none_train.txt"), config)
        test_set = pd.read_csv("dataset/none_test.txt")
        instance = test_set.iloc[3]
        logger.info(f"{instance.values} -> {cb.predict(model, instance)}")

        gc.collect()

        logger.info("-------------------------")

    logger.info("-------------------------")
    logger.info("unit tests completed successfully...")
