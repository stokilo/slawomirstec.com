<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Autocomplete search with Cloudflare KV storage">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/01/kv-search.jpg"
                            class-name="responsive border-0 card-img-top mb-3" alt="Autocomplete search with Cloudflare KV"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Autocomplete</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Autocomplete search on top of Cloudflare KV storage</h3>
                <p></p>

                <p>
                 I've decided to add an autocomplete select field into my sample project. It is quite a common requirement even
                 for small applications. I wanted to know how to do it in a serverless way and keep my budget within limits.
                </p>
                <p>
                I downloaded a list of all Polish streets with 244,226 entries. I think it is an appropriate size for testing
                response times. Functionality is limited only to the search, the user must enter a minimum of 3 characters to trigger
                a search request. The results are limited to 10 entries for each search term.
                </p>
                <p>
                My backend is hosted on the AWS cloud. To implement an autocomplete, I would have to add ElasticSearch to my stack.
                Unfortunately, I am not eligible for the free tier for this service anymore. The minimal cost of running autocomplete app on production
                and development machines for 1 month is around 60$ (micro instances). Proper setup, according to the AWS guidelines, with
                medium VM instances, and 3 availability zones, will cost around 500$. This is only for PROD
                and varies depending on multiple factors. For my sample application, 60$ would do it. However it would run only a few minutes per
                month, it is simply a waste of money.
                </p>
                <p>
                I've decided to make it simpler and stay away from the ElasticSearch AWS offering. For streets search, it is enough to
                index all unique combinations of terms starting from unique 3 letters long term and ending on 97 (max street length in the data set).
                This combined with storing keys in lower case and replacing special characters should give a pretty decent results.
                </p>
                <p>
                I was thinking of storing all such terms in the DynamoDb and perform a query against it. It had potential in the future to enable
                DAX functionality in case a performance was too low. Additionally, I could enable cache on Cloudflare side for all requests
                going through autocomplete endpoints. When request reach my application, it goes over Cloudflare proxy -> Api Gateway -> Lambda -> DynamoDb.
                None of these steps can't be skipped, pressing each letter requires to go over all application layers. That is both, too slow and expensive
                even considering caching on Cloudflare edge.
                </p>
                <p>
                I decided to use Cloudflare KV storage for all my terms. I'm already using Cloudflare worker instances to host my web application.
                What I needed was only a build/deploy setup to migrate data from my data set (zipped file) to the KV storage.
                To upload files to KV I run the wrangler CLI command with bulk upload parameters. More details on
                official documentation site:
                </p>
                <a href="https://developers.cloudflare.com/workers/cli-wrangler" rel="noopener noreferrer" target="_blank">https://developers.cloudflare.com/workers/cli-wrangler</a>
                <p></p>
                <p>
                The process is quite simple. Firstly, I run a wrangler CLI command to create a namespace i.e. with the name AUTOCOMPLETE_KV.
                In the wrangler command output, I get a namespace id that can be used to upload data into KV. This configuration must be included
                in wrangler.toml, sample below. This is required to include it there to allow your worker to access KV via bind name,
                in my case AUTOCOMPLETE_KV.
                </p>

                <client-only>
                  <highlightjs langugage="javascript" :code="snippet1"/>
                </client-only>

                <p>A sample worker code to perform the search of terms provided in the URL query param using AUTOCOMPLETE_KV storage</p>

                <client-only>
                  <highlightjs langugage="javascript" :code="snippet2"/>
                </client-only>

                <p>
                Screenshots on this page show a UI design, a live version is available after the login.
                I get quite consistent response times. When a term is frequently accessed, it is available in the memory on the Cloudflare edge server,
                response times are less than 60 ms. In other cases, when a term is not used very often, it takes a maximum of 250 ms from my location.
                This is quite good for my use-case. I didn't notice any slowdowns and the search experience is ok for me.
                What is most important, it is a very cheap solution, the pricing for writing 1M entries is with the limit of the Worker Bundled plan (5$).
                Additional usage is very cheap. I set the TTL for my key entries to 1 year, this is data that don't
                change frequently.
                </p>

                <ResizeImageTag resizeTo=1200 src="blog/2021/01/response-time.jpg"
                                class-name="responsive border-0 card-img-top mb-3" alt="Autocomplete response time with KV"/>

                <p></p>
                <p>
                One important note, I have a rate-limiting enabled for all my /api calls. This also applies here, each user
                abusing /api resource will be banned for some fixed amount of time. For obvious reasons, I've increased the number of allowed requests for the autocomplete resource.
                </p>
                <p>
                  To summary, I'm satisfied with the results. I think I will use the KV storage for general configuration data.
                  Of course, this is no-go for a sensitive data.
                </p>
              </div>

            </b-card-body>
          </b-card>
        </b-row>
      </div>
    </b-tab>
  </b-tabs>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import Colxx from '~/components/common/Colxx.vue'
import ResponsiveImageTag from '~/components/common/ResponsiveImageTag.vue'
import ResizeImageTag from "~/components/common/ResizeImageTag.vue";

@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'Implement autocomplete search with Cloudflare KV storage',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'Implement autocomplete with cloudflare KV storage'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'cloudflare, kv, autocomplete, search, fuzzy'
      }
    ]
  }
})
export default class CloudflareKvSearch extends Vue {
  snippet1: String = `

kv_namespaces = [
    { binding = "AUTOCOMPLETE_KV", id = "KV_AUTOCOMPLETE_NAMESPACE_ID" }
]

`

  snippet2: String = `
if (url.hostname === workerDomain &&
    url.pathname === API_ENDPOINT_AUTOCOMPLETE) {

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
            searchResult = searchQuery ? await AUTOCOMPLETE_KV.get(searchQuery) : ""
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
  `


}
</script>

