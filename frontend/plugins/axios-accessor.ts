import {Plugin} from '@nuxt/types'
import {initializeAxios} from '~/utils/api'
import {$token} from "~/utils/api";
import {SERVER_API_ROUTES, NuxtJsRouteHelper} from "~/store/api/routes";

const accessor: Plugin = (context) => {
  // Register $axios reference
  initializeAxios(context.$axios)

  let refreshRequestCount: number = 0;

  // Keep refresh token claim 'exp' two times longer than session token
  // Call refresh token to get new short lived jwt, do it before request itself, do it only when jwt is expired
  // Keep request count around to avoid infinite loop
  context.$axios.interceptors.request.use(
    async config => {

      if (config.url != SERVER_API_ROUTES.ROUTE_REFRESH_TOKEN &&
        config.method != "options" &&
        !NuxtJsRouteHelper.isUnauthenticatedApiRoute(config.url!) &&
        !$token.hasValidJwtToken() &&
        refreshRequestCount < 10) {

        refreshRequestCount++
        let tokenRefreshed: boolean = await $token.callRefreshTokenEndPoint()

        if (!tokenRefreshed) {
          context.redirect(NuxtJsRouteHelper.getDefaultRedirectRoute())
        }
      }

      if ($token.getJwt()) {
        if (!NuxtJsRouteHelper.isAwsDirectCall(config.url)) {
          config.headers['Authorization'] = $token.getJwt();
        }
      }
      return config;
    },
    async error => {
      Promise.reject(error)
    });

};

export default accessor
