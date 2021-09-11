import {getAssetFromKV, mapRequestToAsset} from '@cloudflare/kv-asset-handler'

/**
 * The DEBUG flag will do two things that help during development:
 * 1. we will skip caching on the edge, which makes it easier to
 *    debug.
 * 2. we will return an error message on exception in your Response rather
 *    than the default 404.html page.
 */
const DEBUG = false
// Domain connected to the worker instance
const workerDomain = DOMAIN
// AWS regions where API Gateway is deployed
const apiGatewayRegion = REGION
// AWS API Gateway id that is part of URL we proxy using cloudflare workers
const apiGatewayId = REST_API_ID
// Google reCAPTCHA secret key used for api resources that absolutely require human input
const reCaptchaSecretKey = RECAPTCHA
// secret key to check if this is admin call
const adminSecretKey = ADMIN_SECRET_KEY
// allowed ip for admin access
const adminIp = ADMIN_IP
// header name that should contain secret key for admin access
const admin_access_header_name = "PyAws-Admin-Access-Secret"
// header name that should request access without captcha validation
const admin_access_header_name_skip_captcha = "PyAws-Admin-Access-SkipCaptcha"

// endpoints protected by recaptcha
const API_ENDPOINT_CONTACT = '/api/contact'
const API_ENDPOINT_SIGNUP = '/api/auth/signup'
const API_ENDPOINT_LOGIN = '/api/auth/login'
// test autocomplete
const API_ENDPOINT_AUTOCOMPLETE = '/api/autocomplete'
const API_ENDPOINT_CACHE_APPOINTMENT = '/api/appointment/cached'


addEventListener('fetch', event => {
    try {
        event.respondWith(handleEvent(event))
    } catch (e) {
        if (DEBUG) {
            return event.respondWith(
                new Response(e.message || e.toString(), {
                    status: 500,
                }),
            )
        }
        event.respondWith(new Response('Internal Error', {status: 500}))
    }
})


// We support the GET, POST, HEAD, and OPTIONS methods from any origin,
// and accept the Content-Type header on requests. These headers must be
// present on all responses to all CORS requests. In practice, this means
// all responses to OPTIONS or POST requests.
const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

async function handleEvent(event) {
    const url = new URL(event.request.url)
    const requestMethod = event.request.method
    let domainHttps = "https://" + workerDomain;

    try {
        const is_api_endpoint_autocomplete = url.pathname === API_ENDPOINT_AUTOCOMPLETE
        const is_api_endpoint_cache_appointment = url.pathname === API_ENDPOINT_CACHE_APPOINTMENT
        if (url.hostname === workerDomain &&
            (is_api_endpoint_autocomplete || is_api_endpoint_cache_appointment)) {

            if (requestMethod === 'OPTIONS') {
                return new Response(null, {
                    status: 200,
                    headers: corsHeaders
                })
            }
            if (requestMethod === 'GET') {
                let searchResult = ""
                try {
                    const {searchParams} = new URL(event.request.url)
                    let searchQuery = searchParams.get('q')

                    if (is_api_endpoint_autocomplete) {
                        searchResult = searchQuery ? await AUTOCOMPLETE_KV.get(searchQuery) : ""
                    } else if (is_api_endpoint_cache_appointment) {
                        searchResult = searchQuery ? await CACHE_KV.get(searchQuery) : ""
                    }
                    searchResult = searchResult && searchResult.length ? searchResult : ""
                }catch(e){
                    if (DEBUG) {
                        console.log(e.message)
                    }
                }
                return new Response(searchResult, {
                    status: 200,
                    headers: {
                        "Content-Type": "application/json",
                        ...corsHeaders,
                    }})
            }
        }

        if (requestMethod === 'POST' &&
            url.hostname === workerDomain &&
            (url.pathname === API_ENDPOINT_CONTACT ||
                url.pathname === API_ENDPOINT_SIGNUP ||
                url.pathname === API_ENDPOINT_LOGIN)) {

            const requestBody = await event.request.clone().json()

            // admin access is combination if src ip of the caller and special header that should contain
            // secret for admin access
            let adminAccessMode = false
            const clientIP = event.request.headers.get("CF-Connecting-IP")
            let adminSecretKeyFromRequest = event.request.headers.has(admin_access_header_name) ?
                event.request.headers.get(admin_access_header_name) : ""
            if (clientIP === adminIp &&
                adminSecretKeyFromRequest.length > 0 &&
                adminSecretKeyFromRequest === adminSecretKey) {
                adminAccessMode = true
            }

            let validateCaptcha = true
            if (event.request.headers.has(admin_access_header_name_skip_captcha) && adminAccessMode) {
                validateCaptcha = false
            }

            if (validateCaptcha) {
                let recaptchaToken = requestBody.recaptcha.token
                let googleValidateUrl = `https://www.google.com/recaptcha/api/siteverify?secret=${reCaptchaSecretKey}&response=${recaptchaToken}`
                const recaptchaResponse = await fetch(googleValidateUrl, {method: 'POST'})
                const recaptchaBody = await recaptchaResponse.json()
                if (recaptchaBody.success !== true) {
                    return new Response('reCAPTCHA verification failed', {status: 400})
                }
            }

        }
    } catch (e) {
        // captcha must be validated before any request can be passed to Api Gateway
        if (DEBUG) {
            return new Response(e.message || e.toString(), {status: 500})
        } else {
            return new Response("", {status: 500})
        }
    }

    // here we have policy on Api Gateway to only allow request from Cloudflare IP range
    if (url.host === workerDomain &&
        url.origin === domainHttps) {

        const apiWorkerEndPoint = domainHttps + "/api/";
        const apiGatewayEndPoint = `https://${apiGatewayId}.execute-api.${apiGatewayRegion}.amazonaws.com/v1/`;

        if (url.href.substring(0, apiWorkerEndPoint.length) === apiWorkerEndPoint) {
            let apiGateWayUrl = url.href.replace(apiWorkerEndPoint, apiGatewayEndPoint);
            url.hostname = apiGateWayUrl;
            const init = {
                body: event.request.body,
                method: event.request.method,
                headers: event.request.headers
            }
            return await fetch(apiGateWayUrl, init);
        }
    }

    try {
        let options = {}
        // customize caching
        if (DEBUG) {
            options.cacheControl = {
                bypassCache: true,
            }
        } else {
            options.cacheControl = {
                browserTTL: 0,
                edgeTTL: 0,
                bypassCache: false
            }
        }
        // @see https://stackoverflow.com/questions/64254291/cache-control-headers-in-a-cloudflare-workers-site
        const filesRegex = /(.*\.(ac3|avi|bmp|br|bz2|css|cue|dat|doc|docx|dts|eot|exe|flv|gif|gz|ico|img|iso|jpeg|jpg|js|json|map|mkv|mp3|mp4|mpeg|mpg|ogg|pdf|png|ppt|pptx|qt|rar|rm|svg|swf|tar|tgz|ttf|txt|wav|webp|webm|webmanifest|woff|woff2|xls|xlsx|xml|zip))$/
        const filesRegexHtml = /(.*\.(html|html))$/
        if (url.pathname.match(filesRegex)) {
            options.cacheControl.edgeTTL = 3600
            options.cacheControl.browserTTL = 3600
        }

        const page = await getAssetFromKV(event, options)

        // allow headers to be altered
        const response = new Response(page.body, page)

        response.headers.set('X-XSS-Protection', '1; mode=block')
        response.headers.set('X-Content-Type-Options', 'nosniff')
        response.headers.set('X-Frame-Options', 'DENY')
        response.headers.set('Referrer-Policy', 'unsafe-url')
        response.headers.set('Feature-Policy', 'none')
        if (url.pathname === "/") {
            //rewrite utf8 to utf-8
            response.headers.set('Content-Type', 'text/html; charset=utf-8')
        }

        return response

    } catch (e) {
        try {
            let notFoundResponse = await getAssetFromKV(event, {
                mapRequestToAsset: req => new Request(`${new URL(req.url).origin}/not-found/index.html`, req),
            })

            return new Response(notFoundResponse.body, {...notFoundResponse, status: 200})
        } catch (ee) {
            return new Response(ee.message || ee.toString(), {status: 500})
        }

        return new Response(e.message || e.toString(), {status: 500})
    }
}


