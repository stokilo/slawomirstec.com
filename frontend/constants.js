let nuxtBaseUrl = "http://localhost:8000"
let nuxtBaseUrlImageCdn = ""
let nuxtBaseUrlApi = "http://localhost:8000"
let isYourDomain = false

if(process.env.NODE_ENV === 'production') {
  nuxtBaseUrl = "https://" + process.env.PYAWS_CLI_DOMAIN
  nuxtBaseUrlImageCdn = "https://" + process.env.PYAWS_CLI_IMAGE_SUBDOMAIN + "." + process.env.PYAWS_CLI_DOMAIN
  nuxtBaseUrlApi = "https://" + process.env.PYAWS_CLI_DOMAIN + "/api"
}

isYourDomain = nuxtBaseUrl.startsWith("https://your-domain.com")

export default {
  isDevMode : (process.env.NODE_ENV !== 'production'),
  nuxtBaseUrl : nuxtBaseUrl,
  nuxtBaseUrlImageCdn : nuxtBaseUrlImageCdn,
  nuxtBaseUrlApi : nuxtBaseUrlApi,
  isYourDomainCom: isYourDomain,
}
