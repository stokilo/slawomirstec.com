<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="Docker python setup">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/01/docker.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="S3"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">Dashboard</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Docker python setup</h3>
                <p>
                This is a documentation post about introducing dockerized python development in the sample application.
                </p>
                <p></p>
                <p>
                  Initial setup for the application required to install the following tools:
                </p>
                <ol>
                  <li>npm</li>
                  <li>yarn</li>
                  <li>aws cli</li>
                  <li>wrangler cli</li>
                  <li>python</li>
                  <li>pyenv</li>
                  <li>pipenv</li>
                  <li>npm and python dependencies (aws cdk, nuxt ...)</li>
                </ol>
                <p></p>
                <p>
                  This was a little mess. I was experimenting with multiple libraries and frameworks in the last few months.
                  It is easy to accidentally add a global dependency to the project or make a mistake and forget to freeze
                  its version. All issues become apparent while moving to another machine or environment. I was aware of this
                  and decided to move everything to docker.
                </p>
                <p>
                  I've decided that a docker image must contain all libraries required for development and building
                  production assembly. Additionally, I've included all python dependencies in it. I decided to keep
                  node_modules shared via volume. I don't change python dependencies too often and I can live with
                  image rebuild in such cases. For node_modules I decided to keep an option to install them outside of
                  the image. I had to do it because of my hardware and docker architecture limitations. Namely, docker
                  volume sharing with mac host is very slow. Installing yarn dependencies takes 10 times longer than
                  on my host. I've tried many solutions but without success, my old MacBook with overdue battery service
                  slowed down too much.
                </p>
                <p></p>
                <p>
                 Below my docker config. It inherits 3.8 python base image. I defined few layers to separate host libs,
                 tools, and python libraries. The image exposes ports for development and debugging. I'm not very experienced
                 with the docker, I've tried to keep it minimal. I had an issue with permissions to a global node and
                 wrangler modules, which I solved by assigning access to everyone.
                </p>

                <client-only>
                  <highlightjs langugage="javascript" :code="snippet1"/>
                </client-only>
                <p></p>
                <p></p>
                <p>
                  I've implemented a startup script to execute docker commands. These commands are presented below.
                  All details with running containers like volumes, port mappings are configured in the script.
                  The top image is a screen shot from running pyaws-cli and chalice in development mode using this script.
                </p>
                <p></p>
                <ResizeImageTag resizeTo=1200 src="blog/2021/01/script.jpg"
                                class-name="responsive border-0 card-img-top mb-3" alt="S3"/>

                <p></p>
                <hr/>
                <p></p>
                <h4>IDE setup</h4>
                <p>
                  I've documented the setup of my IDE for remote debugging pytest tests and chalice.
                  I'm using debugging library 'pydevd-pycharm' for connecting a debugger from the container to the host.
                  All youtube videos are for documentation purposes.
                </p>
                <p></p>
                <p>Configuration of tests running from the host IDE, tests are executed in the docker container.</p>
                <p></p>
                <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/Ho5Gjg65xY8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                <p></p>
                <p>Debugging tests in the previous configuration</p>
                <p></p>
                <div class="video-container">
                  <iframe width="560" height="315" src="https://www.youtube.com/embed/RDB0EB4eFbA" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                <p></p>
                <p>Debugging AWS Chalice running on the docker container. Configuration of 'pydevd-pycharm' library.</p>
                <p></p>
                <div class="video-container">
                  <iframe width="560" height="315" src="https://www.youtube.com/embed/dUT3hrOlJ3s" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
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
    title: 'Docker python setup',
    meta: [
      {hid: 'description', name: 'description', content: 'Python docker setup instructions'},
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'Docker, python, nuxt, AWS'
      }
    ]
  }
})
export default class DockerPythonSetup extends Vue {
  snippet1: String = `
FROM python:3.8-slim as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV AWS_PAGER ""

FROM base AS pyaws-general-libs
RUN apt-get update && apt-get upgrade -y && \\
    apt-get install make unzip libglu1 libxi6 libgconf-2-4 jq curl git sudo nodejs libffi-dev -y && \\
    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash - && \\
    apt-get -y install nodejs && \\
    ln -s /usr/bin/nodejs /usr/local/bin/node && \\
    curl -sL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.1.18.zip" -o "awscliv2.zip"  && \\
    unzip awscliv2.zip &&\\
    sudo ./aws/install

FROM pyaws-general-libs AS pyaws-python-npm-libs
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
RUN mkdir /home/appuser/.node_modules_global && \\
    npm config set prefix=$HOME/.node_modules_global && \\
    npm set HOME "/home/appuser/" -g && \\
    chmod 777 /home/appuser/.node_modules_global && \\
    export PATH="$HOME/.node_modules_global/bin:$PATH" && \\
    npm config list && \\
    npm i npm@latest -g && \\
    mkdir -p "$HOME/.wrangler" && chmod -R 777 "$HOME/.wrangler" && \\
    npm i @cloudflare/wrangler@1.13.0 -g && \\
    npm i yarn@1.22.10 -g && \\
    yarn global add aws-cdk@1.86.0 && \\
    yarn global add nuxt@2.14.12 && \\
    pip3 install --upgrade pip && \\
    pip3 install pipenv

FROM pyaws-python-npm-libs AS pyaws-cli-app
USER appuser
COPY Pipfile .
COPY Pipfile.lock .
ENV PATH="/home/appuser/.venv/bin:/home/appuser/.local/bin:/home/appuser/.node_modules_global/bin:$PATH"
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync --dev

EXPOSE 8000
EXPOSE 3000
EXPOSE 8090

  `
}
</script>

