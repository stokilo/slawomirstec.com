import constants from "./constants";

console.info("---- nuxt-js isDevMode: " + constants.isDevMode)
console.info("---- nuxt-js nuxtBaseUrl: " + constants.nuxtBaseUrl)
console.info("---- nuxt-js nuxtBaseUrlApi: " + constants.nuxtBaseUrlApi)


export default {
  ssr: true,
  target: "static",
  router: {
    base: constants.isDevMode ? '/' : '/',
    mode: 'history',
    middleware: 'auth',
    prefetchLinks: false
  },
  /*
  ** Headers of the page
  */
  head: {
    htmlAttrs: {
      lang: 'en'
    },
    titleTemplate: '%s - serverless AWS applications',
    title: 'Slawomir Stec',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0, shrink-to-fit=no'},
      {hid: 'description', name: 'description', content: 'Simple AWS serverless applications, personal blog, NuxtJs Vue Lambda Chalice sandbox.'},
      {hid: 'keywords', name: 'keywords', content: 'AWS, serverless, VueJs, Vue, Nuxt, NuxtJs, Javascript, software, dynamodb, Lambda, Chalice, Slawomir Stec, programming, development, ApiGateway, CloudWatch' }
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'}
    ],
    bodyAttrs: {
      class: 'rounded'
    }
  },
  /*
  ** Customize the progress-bar color
  */
  loadingIndicator: {
    name: 'pulse',
    color: '#3B8070',
    background: 'white'
  },
  /*
  ** Global CSS
  */
  css: [
    '~/assets/css/themes/piaf.light.bluenavy.scss'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    {src:'~/plugins/i18n.js', ssr:true},
    {src:'~/plugins/overlay.ts', ssr:true},
    {src:'~/plugins/axios-accessor.ts', ssr:false},
    {src:'~/plugins/vee-validate.js', ssr:false},
    {src:'~/plugins/perfect-scrollbar.ts', ssr:true},
    {src:'~/plugins/vue-select.js', ssr:true},
    {src:'~/plugins/notification.js', ssr:false},
    {src:'~/plugins/highlight.js', ssr:true},
    {src:'~/plugins/calendar.js', ssr:false, mode: 'client'},
    {src:'~/plugins/date-picker.js', ssr:false, mode: 'client'}
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxt/typescript-build',  '@aceforth/nuxt-optimized-images', '@nuxtjs/google-analytics'
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/axios', 'bootstrap-vue/nuxt', '@nuxtjs/recaptcha', '@nuxtjs/robots', '@nuxtjs/sitemap', '@nuxtjs/google-fonts'
  ],
  robots: [
    {UserAgent: '*', Disallow: '/api'},
    {UserAgent: '*', Disallow: '/login'},
    {UserAgent: '*', Disallow: '/signup'},
    {UserAgent: '*', Disallow: '/logout'},
    {UserAgent: '*', Disallow: '/app'},
    {Sitemap: `${constants.nuxtBaseUrl}/sitemap.xml`}
  ],
  sitemap: {
    hostname: constants.nuxtBaseUrl,
    gzip: true,
    exclude: [
      '/api',
      '/api/**',
      '/login',
      '/signup',
      '/logout',
      '/app',
      '/app/**'
    ]
  },
  googleFonts: {
    families: {
      'Nunito': true
    },
    download: true,
    fontsDir: 'fonts',
    fontsPath: '~assets/fonts'
  },
  bootstrapVue: {
    bootstrapCSS: true,
    bootstrapVueCSS: false,
    icons: false,
    components: ['BDropdown', 'BDropdownItem', 'BRow', 'BCol', 'BTabs', 'BTab', 'BCard', 'BButton', 'BCardBody',
                 'BPagination', 'BBadge', 'BButtonGroup', 'BModal', 'BForm', 'BFormGroup', 'BFormInput', 'BBadge',
                 'BFormFile', 'BInputGroup', 'BInputGroupPrepend',
                 'BFormCheckbox', 'BFormRadioGroup', 'BFormTextarea', 'BIconCalendar', 'BIconPerson', 'BIconMailbox',
                 'BIconHouse', 'BIconCollection', 'BIconLayoutSidebar', 'BIconCardChecklist', 'BIconHandThumbsDown',
                 'BIconHandThumbsUp', 'BIconCheckAll', 'BIcon', 'BIconChevronLeft', 'BIconChevronRight',
                 'BIconChevronBarLeft', 'BIconChevronBarRight', 'BIconSearch', 'BIconGithub', 'BIconFacebook', 'BIconMenuButton',
                 'BIconCloudUpload', 'BIconCalendarRange'],
    directives: ['VBModal']
  },
  recaptcha: {
    siteKey: '',
    size: 'compact',
    hideBadge: false,
    version: 2
  },
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: constants.nuxtBaseUrlApi
  },
  proxy: {
    '/api': constants.nuxtBaseUrlApi
  },

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
      config.output.publicPath = './_nuxt/'
    },
    analyze: false,
    babel: {
      compact: true
    },
    parallel: true,
    cache: true,
    hardSource: constants.isDevMode
  },

  components: false,

  optimizedImages: {
    optimizeImages: true,
    optimizeImagesInDev: false
  },
  env: {
    isDevMode: constants.isDevMode,
    nuxtBaseUrl: constants.nuxtBaseUrl,
    nuxtBaseUrlImageCdn: constants.nuxtBaseUrlImageCdn,
    nuxtBaseUrlApi: constants.nuxtBaseUrlApi
  }
}
