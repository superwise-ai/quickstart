import requests
import pandas as pd


class SuperwiseClient:

    def __init__(self, client_id, secret, customer):
        self.client_id = client_id
        self.secret = secret
        self.customer = customer

    def start_session(self):
        self.access_token = self._get_access_token()
        self.HEADERS = {'Authorization': f'Bearer {self.access_token}'}
        self.URL_PREFIX = f"https://portal.superwise.ai/{self.customer}"

    def _get_access_token(self):
        token_url = "https://auth.superwise.ai/identity/resources/auth/v1/api-token"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "clientId": self.client_id,
            "secret": self.secret
        }

        res = requests.post(token_url, json=payload, headers=headers)
        res.raise_for_status()
        token = res.json()['accessToken']

        return token

    def get_tasks_df(self):
        request_url = f'{self.URL_PREFIX}/admin/v1/tasks'

        res = requests.get(request_url, headers=self.HEADERS)
        res.raise_for_status()
        tasks_df = pd.DataFrame(res.json())

        return tasks_df

    def get_features(self, version_id):
        request_url = f'{self.URL_PREFIX}/model/v1/versions/{version_id}/data_entities'

        res = requests.get(request_url, headers=self.HEADERS)
        res.raise_for_status()
        features = pd.DataFrame(res.json())

        version_entities = pd.DataFrame(res.json(), columns=["data_entity", "feature_importance"])
        flatten_version_entities = pd.json_normalize(version_entities["data_entity"], max_level=0)
        flatten_version_entities["feature_importance"] = version_entities["feature_importance"]
        empty_flatten_version_entities = pd.DataFrame(
            columns=["id", "name", "role", "type", "secondary_type", "summary", "dimension_start_ts"]
        )

        features = empty_flatten_version_entities.append(flatten_version_entities)

        return features

    def get_metrics(self):
        request_url = f'{self.URL_PREFIX}/kpi/v1/metrics-functions'

        res = requests.get(request_url, headers=self.HEADERS)
        res.raise_for_status()
        metrics = pd.DataFrame(res.json())

        return metrics

    def get_metrics_values(self, task_id, version_id, entity_id, features):
        request_url = f'{self.URL_PREFIX}/kpi/v1/metrics'
        requests_params = dict(task_id=task_id, version_id=version_id, entity_id=entity_id, segment_id=-1,
                               metric_id=[1], time_unit='D')

        res = requests.get(request_url, params=requests_params, headers=self.HEADERS)
        res.raise_for_status()

        results_df = pd.DataFrame(res.json())
        results_df['entity_name'] = results_df['entity_id'].map(features.set_index('id')['name'].to_dict())
        results_df['date_hour'] = pd.to_datetime(results_df['date_hour'])

        return results_df
