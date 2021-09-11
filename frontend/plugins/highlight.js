import Vue from 'vue'
import hljs from 'highlight.js/lib/core';
import javascript from 'highlight.js/lib/languages/javascript';
import python from 'highlight.js/lib/languages/python';
import xml from 'highlight.js/lib/languages/xml';
import 'highlight.js/styles/github.css';

const accessor = () => {
  hljs.registerLanguage('xml', javascript);
  hljs.registerLanguage('javascript', javascript);
  hljs.registerLanguage('python', python);
  Vue.use(hljs.vuePlugin);
};

export default accessor
