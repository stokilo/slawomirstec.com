import { NuxtAxiosInstance } from '@nuxtjs/axios'
import RefreshToken from "~/store/model/auth/refresh-token";
import AuthService from "~/store/api/auth/auth-service"

class Token {

  private jwt : string;
  private refreshToken: string;

  constructor() {
    this.jwt = "";
    this.refreshToken = "";
  }

  reset() {
    this.setJwt("")
    this.setRefreshToken("")
  }

  setJwt(jwt: string) {
    this.jwt = jwt
  }

  getJwt(): string {
    return this.jwt
  }

  setRefreshToken(refreshToken: string){
    this.refreshToken = refreshToken;
  }

  getRefreshToken(): string {
    return this.refreshToken
  }

  hasValidJwtToken(): boolean {
    return this.isTokenValid(this.getJwt())
  }

  hasValidRefreshToken(): boolean {
    return this.isTokenValid(this.getRefreshToken())
  }

  isTokenValid(token: string): boolean {
    if (!token || token.length <= 0) {
      return false
    }

    let isJwtExpired;
    try{
      let claims = JSON.parse(atob(token.split('.')[1]))
      let exp = claims["exp"];
      const now = Date.now().valueOf() / 1000
      isJwtExpired = exp < now;
    } catch (e) {
      isJwtExpired = true
    }
    return !isJwtExpired
  }

  async callRefreshTokenEndPoint(): Promise<boolean>{
    let success = false
    try {
      let authService: AuthService = new AuthService();
      let result = await authService.refreshToken(new RefreshToken(this.getRefreshToken()))
      if(result.status.success){
        this.setJwt(result.auth.jwt)
        this.setRefreshToken(result.auth.refresh_token)
        success = true
      }
    } catch (error) {
      this.setJwt("")
      this.setRefreshToken("")
    }
    return success
  }
}



let $axios: NuxtAxiosInstance;
let $token: Token = new Token()
let $loader: any;
let $i18n: any
let $notify: any

export function initializeAxios(axiosInstance: NuxtAxiosInstance) {
  $axios = axiosInstance
  $token = new Token()
}

export function initializeLoader(loader: any) {
  $loader = loader;
}

export function initializeI18n(i18n: any) {
  $i18n = i18n;
}

export function initializeNotify(notify: any) {
  $notify = notify;
}

export { $axios, $loader, $i18n, $token, $notify}
