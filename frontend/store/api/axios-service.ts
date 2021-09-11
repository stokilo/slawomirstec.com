import {$axios, $i18n} from "~/utils/api";
import {WithFromJson, Status} from "~/store/model/shared";

interface AxiosConfig {
  headers: Record<string, string>
  timeout: number
}

/**
 * Generic base service to make API calls using axios lib. It provides high level function
 * to invoke WS and process result.
 */
export default class AxiosService {

  AXIOS_JSON_POST_CONFIG: AxiosConfig = {
    headers: {"Content-Type": "application/json"},
    timeout: 15_000
  }

  getRequestConfig(): Object {
    let config = {...this.AXIOS_JSON_POST_CONFIG}
    config.headers["X-Language"] = $i18n.locale
    return config
  }

  async genericFetch<T extends WithFromJson>(routePath: string, model: T, params: object = {}): Promise<T> {
    return $axios.get<T>(routePath, {...this.getRequestConfig(), params})
      .then(function (r) {
        return model.fromJson(r.data)
      })
      .catch(function (error) {
        return model
      })
  }

  async genericPost<R extends { status: Status } & WithFromJson, M extends WithFromJson>(routePath: string, model: M, response: R): Promise<R> {
    return $axios.post<R>(routePath, JSON.stringify(model), this.getRequestConfig())
      .then(function (r) {
        return response.fromJson(r.data);
      })
      .catch(function (error) {

        if (error.response && response.isObjectWithKey(error.response.data, "status")) {
          return response.fromJson(error.response.data)
        }

        response.status.success = false
        response.status.error_message = $i18n.t("api.general-error")

        return response;
      })
  }


}
