<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab :title="$t('piaf.profile')">
      <b-row>
        <Colxx xxs="12" lg="4" class="mb-4 col-left">
          <b-card no-body class="mb-4">

            <ImageTag src="profile.jpg" className="card-img-top" alt="Profile image" />
            <b-card-body>
              <p class="text-muted text-small mb-2">About me</p>
              <p class="mb-3">
                I'm a software developer and technical manager, currently employed for ConSol MENA.
                This website is a live version of the system that I built using serverless services on AWS platform.
                Please feel free to contact me if you would like to know more about using serverless services.
              </p>
              <p class="text-muted text-small mb-2">{{ $t("piaf.location") }}</p>
              <p class="mb-3">Dubai, UAE</p>
              <p class="text-muted text-small mb-2">Responsibilities</p>
              <p class="mb-3">
                <b-badge variant="outline-secondary" class="mb-1 mr-1" pill>BACKEND</b-badge>
                <b-badge variant="outline-secondary" class="mb-1 mr-1" pill>FRONTEND</b-badge>
                <b-badge variant="outline-secondary" class="mb-1 mr-1" pill>PROJECT MANAGEMENT
                </b-badge>
              </p>

              <p class="text-muted text-small mb-2">Website info</p>
              <p class="mb-3">
                This is my blog and sandbox for running serverless applications hosted on AWS and Cloudflare.
                Build with: Nuxt, Vue, Chalice, AWS Lambda, ApiGateway, DynamoDb, Cloudflare workers.
                I write about each framework and libraries that are a part of sample application, this website
                is combination of documentation of the project and personal blog. To start, checkout 'Live Apps Preview' button
                on the top.
              </p>

              <p class="text-muted text-small mb-2">Social</p>
              <div class="social-icons">
                <ul class="list-unstyled list-inline">
                  <li class="list-inline-item">
                    <a href="https://www.facebook.com/slawomir.stec.poland" rel="noopener noreferrer" target="_blank">
                      <b-icon icon="facebook" variant="primary"/>
                    </a>
                  </li>
                  <li class="list-inline-item">
                    <a href="https://github.com/stokilo" rel="noopener noreferrer" target="_blank">
                      <b-icon icon="github" variant="primary"/>
                    </a>
                  </li>
                </ul>
              </div>
            </b-card-body>
          </b-card>
        </Colxx>

        <Colxx xxs="12" lg="8" class="mb-4 col-right">

          <b-row>

            <Colxx v-for="(product,productIndex) in blogItems" xxs="12" lg="6" class="mb-5" :key="`product_${product.id}`">
              <b-card class="flex-row listing-card-container" no-body>
                <div class="w-40 position-relative">
                  <router-link :to="product.link">
                    <ResizeImageTag :resizeTo="product.resizeTo" :src="product.img" :alt="product.title" className="card-img-left"/>
                    <b-badge variant="primary" pill class="position-absolute badge-top-left">{{product.pillText}}</b-badge>
                  </router-link>
                </div>
                <div class="w-60 d-flex align-items-center">
                  <b-card-body>
                    <router-link :to="product.link">
                      <h2 class="mb-3 listing-heading">{{ product.title }}</h2>
                    </router-link>
                    <p class="listing-desc text-muted">{{ product.initialText }}</p>
                  </b-card-body>
                </div>
              </b-card>
            </Colxx>
          </b-row>

          <b-row>
            <br/>
          </b-row>

          <b-row>
            <Colxx xxs="12">
              <b-pagination class="justify-content-center pagination"
                                v-model="currentPage"
                                :per-page="this.pageSize"
                                :total-rows="getTotalRows"
                                align="center">
                <template v-slot:next-text>
                  <b-icon icon="chevron-right" font-scale="1.5" />
                </template>
                <template v-slot:prev-text>
                  <b-icon icon="chevron-left" font-scale="1.5"  />
                </template>
                <template v-slot:first-text>
                  <b-icon icon="chevron-bar-left" font-scale="1.5"  />
                </template>
                <template v-slot:last-text>
                  <b-icon icon="chevron-bar-right" font-scale="1.5"  />
                </template>
              </b-pagination>
            </Colxx>
          </b-row>

        </Colxx>
      </b-row>
    </b-tab>

    <b-tab :title="$t('piaf.interests')">
      <div class="card-body">
        <h2 class="card-title">What I do?</h2>

        <div class="scroll">
          <div class="d-flex flex-row mb-3">
            <a class="d-block position-relative" href="#">
              <img src="~/static/icons/management.svg?original" alt="Management" class="list-thumbnail border-0">
              <span
                class="badge badge-pill badge-theme-2 position-absolute badge-top-right">SOLID</span>
            </a>
            <div class="pl-3 pt-2 pr-2 pb-2">
              <a href="#">
                <p class="list-item-heading">Project Management</p>
                <div class="pr-4 d-sm-block">
                  <p class="text-muted mb-1 text-small">8 years experience</p>
                </div>
                <div class="text-primary text-small font-weight-medium d-sm-block">
                  Technical project lead for 8+ years.
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="scroll">
          <div class="d-flex flex-row mb-3">
            <a class="d-block position-relative" href="#">
              <img src="~/static/icons/java.svg?original" alt="Java" class="list-thumbnail border-0">
              <span
                class="badge badge-pill badge-theme-2 position-absolute badge-top-right">SOLID</span>
            </a>
            <div class="pl-3 pt-2 pr-2 pb-2">
              <a href="#">
                <p class="list-item-heading">Java</p>
                <div class="pr-4 d-sm-block">
                  <p class="text-muted mb-1 text-small">8 years experience</p>
                </div>
                <div class="text-primary text-small font-weight-medium d-sm-block">
                  Spring Boot, Quarkus ...
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="scroll">
          <div class="d-flex flex-row mb-3">
            <a class="d-block position-relative" href="#">
              <img src="~/static/icons/javascript.svg?original" alt="JavaScript" class="list-thumbnail border-0">
              <span
                class="badge badge-pill badge-theme-2 position-absolute badge-top-right">SOLID</span>
            </a>
            <div class="pl-3 pt-2 pr-2 pb-2">
              <a href="#">
                <p class="list-item-heading">JavaScript</p>
                <div class="pr-4 d-sm-block">
                  <p class="text-muted mb-1 text-small">10 years experience</p>
                </div>
                <div class="text-primary text-small font-weight-medium d-sm-block">
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="scroll">
          <div class="d-flex flex-row mb-3">
            <a class="d-block position-relative" href="#">
              <img src="~/static/icons/coldfusion.svg?original" alt="Coldfusion" class="list-thumbnail border-0">
              <span
                class="badge badge-pill badge-theme-2 position-absolute badge-top-right">SOLID</span>
            </a>
            <div class="pl-3 pt-2 pr-2 pb-2">
              <a href="#">
                <p class="list-item-heading">Coldfusion</p>
                <div class="pr-4 d-sm-block">
                  <p class="text-muted mb-1 text-small">9 years experience</p>
                </div>
                <div class="text-primary text-small font-weight-medium d-sm-block">
                  Coldfusion web app and backend development
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="scroll">
          <div class="d-flex flex-row mb-3">
            <a class="d-block position-relative" href="#">
              <img src="~/static/icons/python.svg?original" alt="Python" class="list-thumbnail border-0">
              <span
                class="badge badge-pill badge-theme-2 position-absolute badge-top-right">GOOD</span>
            </a>
            <div class="pl-3 pt-2 pr-2 pb-2">
              <a href="#">
                <p class="list-item-heading">Python</p>
                <div class="pr-4 d-sm-block">
                  <p class="text-muted mb-1 text-small">2 years experience, CLI tools and AWS
                    lambda</p>
                </div>
                <div class="text-primary text-small font-weight-medium d-sm-block">
                  AWS chalice, AWS CDK, Pynamodb
                </div>
              </a>
            </div>
          </div>
        </div>

        <div class="scroll">
          <div class="d-flex flex-row mb-3">
            <a class="d-block position-relative" href="#">

              <img src="~/static/icons/vue.svg?original" alt="Vue" class="list-thumbnail border-0">
              <img src="~/static/icons/vim.svg?original" alt="Vim" class="list-thumbnail border-0">
              <img src="~/static/icons/intellij.svg?original" alt="Intellij" class="list-thumbnail border-0">
              <img src="~/static/icons/aws.svg?original" alt="AWS" class="list-thumbnail border-0">

            </a>
            <div class="pl-3 pt-2 pr-2 pb-2">
              <a href="#">
                <p class="list-item-heading">Various others</p>
                <div class="pr-4 d-sm-block">
                  <p class="text-muted mb-1 text-small"></p>
                </div>
                <div class="text-primary text-small font-weight-medium d-sm-block">
                  Maven, Gradle, Ant, AngularJS, Elixir, MSSQL, Hibernate, ..
                </div>
              </a>
            </div>
          </div>
        </div>

        <br/>
        <a href="https://devicon.dev/" rel="noopener noreferrer" target="_blank">Dev icons by https://devicon.dev/</a>
        <br/>
        <a href="https://iconscout.com/icons/intellij" rel="noopener noreferrer" target="_blank">Intellij Icon</a> by <a href="https://iconscout.com/contributors/icon-mafia">Icon Mafia</a> on <a href="https://iconscout.com" rel="noopener noreferrer">Iconscout</a>
        <br/>
        <a href="https://iconscout.com/icons/management" rel="noopener noreferrer" target="_blank">Management Icon</a> by <a href="https://iconscout.com/contributors/jemismali" target="_blank" rel="noopener noreferrer">Jemis Mali</a>
      </div>
    </b-tab>

    <b-tab :title="$t('piaf.contact')">
      <div class="card-body">
        <client-only>
          <ContactForm/>
        </client-only>
      </div>
    </b-tab>

  </b-tabs>
</template>

<script lang="ts">
import Component from "vue-class-component";
import Vue from "vue";
import Colxx from '~/components/common/Colxx.vue'
import ImageTag from '~/components/common/ImageTag.vue'
import ResponsiveImageTag from "~/components/common/ResponsiveImageTag.vue";
import ResizeImageTag from "~/components/common/ResizeImageTag.vue";
import ContactForm from "~/components/forms/ContactForm.vue";
import ViewportResolution from "~/store/model/client";

@Component({
  components: {
    ImageTag,
    ResponsiveImageTag,
    ResizeImageTag,
    Colxx,
    ContactForm
  }
})
export default class Profile extends Vue {
  currentPage: number = 1
  pageSize: number = 6
  products: Array<Object> = [
    {
      "id": "sst-nuxtjs",
      "createDate": "2021/09/10",
      "title": "SST + Typescript + NuxtJs",
      "pillText": "SST",
      "initialText": "Sample application using SST + Typescript + NuxtJs",
      "img": "blog/2021/09/dialog.png",
      "link": "/blog/2021/09/ssttn",
      "resizeTo": "960"
    },
    {
      "id": "cloud9",
      "createDate": "2021/06/24",
      "title": "Cloud9",
      "pillText": "Cloud9",
      "initialText": "Cloud9 quick review",
      "img": "blog/2021/06/cloud9.png",
      "link": "/blog/2021/06/cloud9",
      "resizeTo": "960"
    },
    {
      "id": "sst-amplify-auth",
      "createDate": "2021/06/07",
      "title": "Serverless stack (SST) + Amplify auth",
      "pillText": "SST",
      "initialText": "Template project for SST + Amplify auth stacks.",
      "img": "blog/2021/06/sst.png",
      "link": "/blog/2021/06/sst",
      "resizeTo": "960"
    },
    {
      "id": "fargate-spring-cicd",
      "createDate": "2021/05/24",
      "title": "Fargate Spring Boot + CI/CD",
      "pillText": "CICD",
      "initialText": "AWS Code Pipeline on example of Fargate Spring Boot application",
      "img": "blog/2021/05/cicd.png",
      "link": "/blog/2021/05/fargate-springboot-cicd",
      "resizeTo": "960"
    },
    {
      "id": "aws-billing-credit",
      "createDate": "2021/05/06",
      "title": "AWS Billing credit",
      "pillText": "AWS",
      "initialText": "AWS credit received.",
      "img": "blog/2021/05/credit-main.png",
      "link": "/blog/2021/05/billing-credit",
      "resizeTo": "960"
    },
    {
      "id": "cdk-aurora-spring-cloud",
      "createDate": "2021/05/02",
      "title": "AWS CDK Aurora Spring Cloud",
      "pillText": "Spring Cloud",
      "initialText": "Aws Aurora RDS and Spring Cloud",
      "img": "blog/2021/05/read-replica-1.png",
      "link": "/blog/2021/05/aurora-spring-cloud",
      "resizeTo": "960"
    },
    {
      "id": "cdk-rds-vpn",
      "createDate": "2021/04/25",
      "title": "AWS CDK RDS + VPN",
      "pillText": "CDK",
      "initialText": "Aws CDK setup for Aurora RDS and Vpn Client",
      "img": "blog/2021/04/rds-vpn.png",
      "link": "/blog/2021/04/cdk-rds-vpn",
      "resizeTo": "960"
    },
    {
      "id": "dynamodb-json-column",
      "createDate": "2021/02/25",
      "title": "Storing JSON as a map attribute in the DynamoDB",
      "pillText": "DynamoDb",
      "initialText": "Example of storing JSON serialized model objects in single column.",
      "img": "blog/2021/02/dynamodb-json.png",
      "link": "/blog/2021/02/dynamodb-json",
      "resizeTo": "960"
    },
    {
      "id": "cloudflare-kv-cache",
      "createDate": "2021/02/14",
      "title": "AWS Cloudflare KV cache",
      "pillText": "KV Cache",
      "initialText": "Caching AWS API using Cloudflare KV storage",
      "img": "blog/2021/02/kv-cache.png",
      "link": "/blog/2021/02/cloudflare-kv-cache",
      "resizeTo": "960"
    },
    {
      "id": "cloudflare-kv-search",
      "createDate": "2021/01/28",
      "title": "Autocomplete with Cloudflare KV",
      "pillText": "Autocomplete",
      "initialText": "Autocomplete search field on top of Cloudflare KV",
      "img": "blog/2021/01/kv-search-main.jpg",
      "link": "/blog/2021/01/cloudflare-kv-search",
      "resizeTo": "960"
    },
    {
      "id": "docker-python",
      "createDate": "2021/01/19",
      "title": "Docker python setup",
      "pillText": "Docker",
      "initialText": "Docker python setup for the sample project",
      "img": "blog/2021/01/docker.png",
      "link": "/blog/2021/01/docker-python",
      "resizeTo": "960"
    },
    {
      "id": "s3",
      "createDate": "2021/01/08",
      "title": "S3 + Cloudflare CDN",
      "pillText": "AWS",
      "initialText": "S3 file upload and integration with Cloudflare CDN",
      "img": "blog/2021/01/s3-main.jpg",
      "link": "/blog/2021/01/s3",
      "resizeTo": "960"
    },
    {
      "id": "artillery",
      "createDate": "2021/01/10",
      "title": "Load testing with artillery",
      "pillText": "Tools",
      "initialText": "Sample load test configuration for artillery tool",
      "img": "blog/2021/01/artillery.jpg",
      "link": "/blog/2021/01/artillery",
      "resizeTo": "960"
    },
    {
      "id": "high-level-overview",
      "createDate": "2020/12/12",
      "title": "High-level overview.",
      "pillText": "AWS",
      "initialText": "Few words about software stack, libraries, and frameworks.",
      "img": "blog/2020/12/high-level.jpg",
      "link": "/blog/2020/12/high-level-overview",
      "resizeTo": "960"
    },
    {
      "id": "dynamodb-model-design",
      "createDate": "2020/12/11",
      "title": "DynamoDB dashboard model.",
      "pillText": "DynamoDB",
      "initialText": "Design of the DynamoDb model for dashboard",
      "img": "blog/2020/12/dashboard.jpg",
      "link": "/blog/2020/12/dynamodb-model-design",
      "resizeTo": "960"
    },
    {
      "id": "deployment",
      "createDate": "2020/12/23",
      "title": "Deployment with CDK and Wrangler",
      "pillText": "AWS-Cloudflare",
      "initialText": "Backend and front-end provisioning",
      "img": "blog/2020/12/deploy.jpg",
      "link": "/blog/2020/12/cdk-wrangler-deployment",
      "resizeTo": "960"
    },
    {
      "id": "piaf-templates",
      "createDate": "2020/12/11",
      "title": "Piaf templates",
      "pillText": "Design",
      "initialText": "Piaf is the combination of good design, quality code, and attention to detail.",
      "img": "blog/2020/12/piaf.jpg",
      "link": "/blog/2020/12/piaf-design",
      "resizeTo": "960"
    },
    {
      "id": "aws-organizations",
      "createDate": "2020/12/22",
      "title": "AWS organizations",
      "pillText": "AWS",
      "initialText": "AWS organization structure for dev and prod environments.",
      "img": "blog/2020/12/org-1.jpg",
      "link": "/blog/2020/12/aws-organizations",
      "resizeTo": "960"
    }
  ];


  get getTotalRows(): number {
    return this.products.length
  }

  get blogItems(): object {
    return this.products.slice((this.currentPage-1) * this.pageSize, (this.currentPage-1) * this.pageSize + this.pageSize)
    // pageSize = 2, item count 4, init currentPage = 1
    // a = [1,2,3,4]
    // currentPage = 1
    // a.slice(0,2) => [1, 2] -> page 1   (currentPage-1) * pageSize, (currentPage-1) * pageSize + pageSize
    //                                    (1-1) * 2 = 0, (1-1) * 2 + 2 = 2
    // currentPage = 2
    // a.slice(2,4) => [3, 4] -> page 2   (currentPage-1) * pageSize, (currentPage-1) * pageSize + pageSize
    //                                    (2-1) * 2 = 2 , (2-1) * 2 + 2 = 4
  }
}

</script>

