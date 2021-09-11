<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Serverless stack (SST) + Typescript + NuxtJs">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/09/login.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="SST"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Serverless stack (SST) + Typescript + NuxtJs</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Serverless framework - TypeScript </h3>
                <p>This year I had very long 'covid' vacations. Once I come back, I've started working on a new project that you can find on my Github:</p>
                <a href="https://github.com/stokilo/aws-sst-typescript-nuxtjs" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-sst-typescript-nuxtjs</a>
                <p></p>
                <p>This is a small SPA with a login and contact page. Authentication is build using Facebook/Google OAuth2 protocol.</p>
                <p>The backend has been written in the Typescript. The infrastructure and development are based on the serverless stack (SST) framework.</p>
                <p>The frontend is done with the Vue, on top of that NuxtJS, and few plugins for image optimization, sitemaps, etc.</p>
                <p>UI components and CSS: Bulma and Buefy libraries.</p>
                <p>The application allows to create a single 'contact' entity in DynamoDB and retrieve a list of them for the currently authenticated user.
                  Nothing fancy going here. The code can be used as a startup template for a small project.</p>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Python lambda VS Typescript lambda</h3>
                <p>The website you are reading now consists of a blog and a sample serverless app (see link on the top).
                  It is implemented using the Chalice framework where only Python language is supported.</p>
                <p>After I've discovered SST and live lambda reload + debugging features I wanted to migrate to javascript.
                  My motivation for doing that:</p>
                <ul>
                  <li>Share Javascript/Typescript codebase on both, backend and client side.</li>
                  <li>Single model for backend and frontend. I don't like to maintain converters and mappers on both sides.</li>
                  <li>I wanted to move to strongly typed language.</li>
                  <li>IMHO Python package and dependency management are worse and slower than Javascript npm/yarn.</li>
                </ul>
                <p></p>
                <p>Most important for me were 1 and 2. To share the models, I've decided to keep them on the backend.</p>
                <a href="https://github.com/stokilo/aws-sst-typescript-nuxtjs/tree/master/src/backend-frontend" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-sst-typescript-nuxtjs/tree/master/src/backend-frontend</a>
                <p></p>
                <p>Mapping is configured under frontend/tsconfig.json file:</p>
                <client-only>
                  <highlightjs langugage="java" :code="snippet1"/>
                </client-only>
                <p></p>
                <p>Here I map backend-frontend folder as @backend, you can access models in the client with the following import </p>
                <client-only>
                  <highlightjs langugage="java" :code="snippet2"/>
                </client-only>
                <p></p>
                <p>This model sharing saves time in development. Additionally, I don't have to maintain converters on both sides. This also leads to fewer bugs
                as forgetting to update one of the sides is not uncommon.</p>
                <p>This is not the end of the story. To keep the model in order, I've introduced the Typescript Zod library for schema validation</p>
                <a href="https://github.com/colinhacks/zod" rel="noopener noreferrer" target="_blank">https://github.com/colinhacks/zod</a>
              </div>
            </b-card-body>

            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Zod schema declaration and validation</h3>
                <p></p>
                <p>Please check the following code snippet that depicts declaration of the Zod type</p>
                <client-only>
                  <highlightjs langugage="java" :code="snippet3"/>
                </client-only>
                <p></p>
                <p>Zod schema declares model object fields, types, and validations.</p>
                <p>Schema can be used to define a type (see <b>TypeOf</b> function usage). </p>
                <p>You can pass an object to the function <b>parse</b>:</p>
                <client-only>
                  <highlightjs langugage="java" :code="snippet4"/>
                </client-only>
                <p>In the given example Zod will throw an error. Mandatory fields are not present in provided object argument. The output of the error
                contains a path to the missing fields and failed checks.</p>
                <p>Having <b>TypeOf</b> in place gives us a model type available for static checks and nice IDE autocompletion.
                  I've integrated Zod library in all places where data is exchanged between client and server side.
                  For example, generic axios functions for get and post requests are using schema like following</p>
                <client-only>
                  <highlightjs langugage="java" :code="snippet5"/>
                </client-only>
                <p></p>
                <p>In order to use it i.e. to fetch Contact form data from the server, you must provide schema and returned type:</p>
                <client-only>
                  <highlightjs langugage="java" :code="snippet6"/>
                </client-only>
                <p></p>
                <p>For simple CRUD applications, it covers a lot of usecases. I did however a brave move and integrated Zod
                 on the backed side (inside DAO layer for DynamoDB).</p>

              </div>
            </b-card-body>


            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">DynamoDb model</h3>
                <p>This time, I've decided to implement my own data access layer for DynamoDB.</p>
                <p>My previous projects were including PynamoDb library for Python.
                Nothing wrong with that, but this time, I wanted to store data for my entities as object literals.
                  I've converted them into DynamoDb map column type. API access is done using DynamoDb Document Client.</p>
                <p>I wanted to keep the database schema as simple as possible. I don't like storing each entity field
                as a DynamoDb column. My entity's objects are small. I calculated that fetching all fields
                  for reading and writing will not cost more RCU/WCU.</p>
                <p>In return, I simplified DAO layer and entity mapping. Code is easier to read. Adding new functionalities takes less time.
                  I validate the objects on the database read and writes.</p>
                <p>Using my own abstraction for the DAO required to choose a strategy for data storage.</p>
                <p>For this simple CRUD, it is a standard single table strategy with entities supporting the following access patterns</p>
                <ul>
                  <li>1. One-to-one fetch/write by unique PK/SK key. </li>
                  <li>2. One-to-many fetch/write by unique PK and SK as KSUID (order by timestamp)</li>
                </ul>
                <p></p>
                <p>You may think this is a very limited set of functionalities. And this is true.</p>
                <p>For such a simple application it is more than enough. Additionally, I think this is a good starter to
                learn about RCU/WCU costs while doing any design decisions. You can enable DynamoDb logs to get JSON stats
                included in the CloudWatch logs. Use Athena to find your RCU/WCU consumed and analyze the access patterns with associated costs.</p>
              </div>
            </b-card-body>


            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">SST</h3>
                <p>Infrastructure is provisioned with the SST framework.</p>
                <p>Check their Slack channel, they have an active and friendly community. Maintainers are online quite often
                  and are very supportive.</p>
                <p>The Serverless Stack includes a lot of interesting tutorials for serverless applications. Check them out, there is a guide for serverless application development.
                It is a thorough introduction with many useful tricks and tips. Their SST documentation contains many examples of how to configure your stack.
                  I've copied most of my stack from these samples and adjusted it to my needs.</p>
                <p>My stack deploys a full serverless application. The frontend is hosted on a predefined domain and cached
                on the Cloudfront. An initial deployment takes 10-20 minutes. SST CLI is very stable and quite fast.
                  You may find some problems if you integrate various AWS services but join the Slack and ask for guidance to find a solution.</p>
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
//@ts-ignore

@Component({
  components: {
    ResizeImageTag,
    ResponsiveImageTag,
    Colxx
  },
  head: {
    title: 'Serverless stack (SST) + Typescript + NuxtJs',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'Template project for SST + Typescript + NuxtJs'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'aws, serverless, stack, sst, typescript, nuxtjs, vue'
      }
    ]
  }
})
export default class SSTTN extends Vue {
  snippet1: String =
`"paths": {
"~/*": ["./*"],
"@/*": ["./*"],
"@backend/*": ["../src/backend-frontend/*"]
},`

  snippet2: String = `import { Contact, newContact, newTestContact } from '@backend/contact'`

  snippet3: String =
`
import * as zod from 'zod'

export const AuthAndRefreshJwtTokenSecretsSchema = zod.object({
  authTokenSecret: zod.string().uuid(),
  refreshTokenSecret: zod.string().uuid()
})
export type AuthAndRefreshJwtTokenSecrets = zod.TypeOf<typeof AuthAndRefreshJwtTokenSecretsSchema>
`

  snippet4: String = `AuthAndRefreshJwtTokenSecretsSchema.parse({})`

  snippet5: String =
    `
 async $get<T, E extends ZodType<T>> (routePath: string, schema: E, params: object = {}): Promise<T | undefined> {
    return await $axios.get(routePath, { ...this.getRequestConfig(), params })
      .then(function (r) {
        return schema.parse(r.data)
      })
      .catch(function (error) {
        $log.error(error)
        return undefined
      })
  }
    `

  snippet6: String = `
const response = await this.axiosService.$get<ContactsFormResponse, typeof ContactsFormResponseSchema>(
      SERVER_API_ROUTES.ROUTE_CONTACT, ContactsFormResponseSchema)
  `
}

</script>
