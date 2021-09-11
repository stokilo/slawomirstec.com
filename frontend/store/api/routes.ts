/**
 * API routes
 */
export enum SERVER_API_ROUTES {
  ROUTE_PATH_AUTH_SIGNUP = "auth/signup",
  ROUTE_PATH_AUTH_PROFILE = "auth/profile",
  ROUTE_LOGIN = "auth/login",
  ROUTE_REFRESH_TOKEN = "auth/refresh",
  ROUTE_CONTACT = 'contact',
  ROUTE_TODO = 'todo',
  ROUTE_DASHBOARD = 'dashboard',
  ROUTE_TODO_BATCH = 'todo/batch',
  ROUTE_UPLOAD = 'upload',
  ROUTE_APPOINTMENT = "appointment",
  ROUTE_APPOINTMENT_CACHED = "appointment/cached",
  ROUTE_LOGOUT = 'logout'
}

export class NuxtJsRouteHelper {

  /**
   * Check if nuxtjs route provided as argument can be accessed without valid auth tokens
   * @param nuxtRouteName this is nuxt route name generated from pages/ folder structure
   */
  static isUnauthenticatedRoute(nuxtRouteName: string): boolean {
    return nuxtRouteName == 'login' || nuxtRouteName == 'signup' ||
      nuxtRouteName == 'index' || nuxtRouteName == 'refresh' || nuxtRouteName == 'not-found';
  }

  /**
   * Check if API route provided as argument can be called without auth tokens
   * @param apiRoute this is path for our app API call
   */
  static isUnauthenticatedApiRoute(apiRoute: string): boolean {
    if(this.isUnauthenticatedKvAccess(apiRoute, SERVER_API_ROUTES.ROUTE_APPOINTMENT_CACHED)) {
      return true
    }

    return apiRoute == SERVER_API_ROUTES.ROUTE_LOGIN ||
      apiRoute == SERVER_API_ROUTES.ROUTE_PATH_AUTH_SIGNUP ||
      apiRoute == SERVER_API_ROUTES.ROUTE_REFRESH_TOKEN ||
      apiRoute == SERVER_API_ROUTES.ROUTE_CONTACT ||
      apiRoute == SERVER_API_ROUTES.ROUTE_APPOINTMENT_CACHED
  }

  static isLogoutRoute(route: string): boolean {
    return route == SERVER_API_ROUTES.ROUTE_LOGOUT
  }

  /**
   * return main page route
   */
  static getIndexRoute(): string {
    return "/"
  }

  /**
   * return route that user should see in case something went wrong
   */
  static getDefaultRedirectRoute(): string {
    return "/login"
  }

  /**
   * return route for the app that requires authenticated access
   */
  static getDefaultAppRoute(): string {
    return "/app/dashboard"
  }

  /**
   * Blog pages don't require authentication
   * @param routePath
   */
  static isBlog(routePath: string): boolean {
    return routePath.startsWith("/blog/")
  }

  /**
   * Axios call to AWS URL i.e. S3 upload
   * @param routePath
   */
  static isAwsDirectCall(routePath: string = ""): boolean {
    return routePath.includes(".amazonaws.com")
  }

  /**
   * Ensures access to KV cache store without authentication
   * @param routePath
   * @param routeToCheck
   */
  static isUnauthenticatedKvAccess(routePath: string, routeToCheck: string) {
    return routePath.startsWith(`https://your-domain.com/api/appointment/cached`)
  }

}





