import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import os


os.environ['SUPERWISE_CLIENT_NAME'] = '' #TODO
os.environ['SUPERWISE_SECRET'] = '' #TODO
os.environ['SUPERWISE_CLIENT_ID'] = '' #TODO


df = pd.read_csv('https://bit.ly/36gldOJ').drop(columns=['Unnamed: 0'])

#print(df.shape)
#print(df.head(3))

X = df.drop(columns="price")
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



categorical_cols = ['cut','clarity','color']
preprocessor = ColumnTransformer(
    transformers=[
        #('drop_id', 'drop', [0]),
        ('categorical',  OneHotEncoder(), [2,3,4]),
    ], remainder='drop')


diamond_price_model=LinearRegression()

my_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', diamond_price_model)
])

X_train = X_train.reset_index()
print(X_train.head(3))
my_pipeline.fit(X_train, y_train)

#y_pred_train =  my_pipeline.predict(X_train)

#X_train = X_train.reset_index()
#print(X_train.head(3))
#print(X_train.to_json())
y_pred_index = my_pipeline.predict(X_train.to_numpy().tolist())

print (y_pred_index)
#baseline_data = X_train.assign(prediction=y_pred_train,ts=pd.Timestamp.now(),price=y_train)
#baseline_data["prediction"] = baseline_data["prediction"].astype(float)
#print(baseline_data.head())



def do_superwise():

    from superwise import Superwise
    from superwise.models.task import Task
    from superwise.models.version import Version
    from superwise.models.data_entity import DataEntity
    from superwise.resources.superwise_enums import TaskTypes,FeatureType,DataTypesRoles

    import os

    myObject = {}
    with open(os.path.expanduser('~/.superwise')) as f:
        for line in f.readlines():
            key, value = line.rstrip("\n").split("=")
            os.environ[key] = value

    sw = Superwise()

    diamond_task =Task(
        task_type=TaskTypes.REGRESSION,
        title="Diamond Model",
        task_description="Regression model which predict the diamond price",
        monitor_delay=1)
    my_task = sw.task.create(diamond_task)
    print(my_task.id)


    schema = [
        DataEntity(
            name="x", type=FeatureType.NUMERIC, role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="y", type=FeatureType.NUMERIC,  role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="z", type=FeatureType.NUMERIC, role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="table", type=FeatureType.NUMERIC, role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="depth", type=FeatureType.NUMERIC,  role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="clarity", type=FeatureType.CATEGORICAL,  role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="color", type=FeatureType.CATEGORICAL, role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="cut", type=FeatureType.CATEGORICAL,  role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="carat", type=FeatureType.NUMERIC,role=DataTypesRoles.FEATURE, feature_importance=None
        ),
        DataEntity(
            name="price", type=FeatureType.NUMERIC,  role=DataTypesRoles.LABEL, feature_importance=None
        ),
        DataEntity(
            name="prediction", type=FeatureType.NUMERIC, role=DataTypesRoles.PREDICTION_VALUE, feature_importance=None
        ),
        DataEntity(
            name="ts", type=FeatureType.TIMESTAMP,role=DataTypesRoles.TIMESTAMP, feature_importance=None
        ),
        DataEntity(
            name="record_id", type=FeatureType.CATEGORICAL, role=DataTypesRoles.ID, feature_importance=None
        ),
    ]


    baseline_df = baseline_data.reset_index().rename(columns={"index": "record_id"})
    print(baseline_df.head())



    diamond_version = Version(
        task_id=my_task.id,
        version_name="DiamondV1",
        baseline_df=baseline_df,
        data_entities=schema,
    )
    my_version = sw.version.create(diamond_version)
    sw.version.activate(my_version.id)


    y_test_pred= my_pipeline.predict(X_test)
    ongoing_prediction = X_test.assign(prediction=y_test_pred,ts=pd.Timestamp.now())
    ongoing_prediction["prediction"] = ongoing_prediction["prediction"].astype(float)


    ongoing_prediction = ongoing_prediction.reset_index().copy().rename(columns={"index": "record_id"})
    ongoing_prediction["task_id"] = my_task.id
    ongoing_prediction["version_id"] = my_version.id
    print(ongoing_prediction.head())


    prediction_file_name = "ongoing_prediction.parquet"
    ongoing_prediction.to_parquet(prediction_file_name)
    sw.data.log_file(file_path=prediction_file_name)


    ongoing_label = y_test.reset_index().copy().rename(columns={"index": "record_id"})
    ongoing_label["task_id"] = my_task.id
    print(ongoing_label.head())

    label_file_name = "ongoing_label.parquet"
    ongoing_label.to_parquet(label_file_name)
    sw.data.log_file(file_path=label_file_name)