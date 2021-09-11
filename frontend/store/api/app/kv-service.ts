import AxiosService from "~/store/api/axios-service";
import {$axios} from "~/utils/api";
import {AppointmentForMonthResult} from "~/store/model/app/appointment";
import {SERVER_API_ROUTES} from "~/store/api/routes";

export default class KvService extends AxiosService {

  /**
   * Query KV autocomplete namespace for Polish streets data
   * @param searchTerm
   */
  async kvStreetsSearch(searchTerm: string) {
    return $axios.get(`${this.resolveHost()}/api/autocomplete?q=${escape(searchTerm)}`)
  }

  /**
   * Query KV cache namespace for appointments data
   * @param year
   * @param month
   */
  async kvAppointments(year: number, month: number): Promise<AppointmentForMonthResult> {
    const kv_key = `__APPOINTMENT__${year}-${month}`
    const url = `${this.resolveHost()}/api/${SERVER_API_ROUTES.ROUTE_APPOINTMENT_CACHED}?q=${escape(kv_key)}`
    return $axios.get(url, this.getRequestConfig())
  }

  /**
   * In development mode we connect to development domain to avoid running wrangler dev command proxy.
   **/
  resolveHost() {
    return process.env.isDevMode ? "https://your-dev-domain.com" : process.env.nuxtBaseUrl
  }

}
