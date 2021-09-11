import Vue from 'vue'
import  { CalendarView, CalendarViewHeader, CalendarMathMixin } from '~/node_modules/vue-simple-calendar/src/components/bundle';

require("vue-simple-calendar/static/css/default.css")
require("vue-simple-calendar/static/css/holidays-us.css")

Vue.use(CalendarView)
Vue.use(CalendarViewHeader)
Vue.use(CalendarMathMixin)
