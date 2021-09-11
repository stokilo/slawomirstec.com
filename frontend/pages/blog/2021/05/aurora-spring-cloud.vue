<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="AWS CDK Aurora RDS and Spring Cloud">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <ResizeImageTag resizeTo=1200 src="blog/2021/05/read-replica-1.png"
                            class-name="responsive border-0 card-img-top mb-3" alt="CDK RDS VPN"/>
            <span
              class="badge badge-pill badge-theme-2 position-absolute badge-top-left">AWS CDK Aurora and Spring Cloud</span>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">AWS CDK Aurora RDS and Spring Cloud</h3>
                <p>Spring Cloud for AWS is part of the Spring Cloud project that I wanted to integrate with CDK Java project
                that I've implemented last week:</p>
                <p></p>
                <a href="https://slawomirstec.com/blog/2021/04/cdk-rds-vpn" rel="noopener noreferrer" target="_blank">https://slawomirstec.com/blog/2021/04/cdk-rds-vpn</a>
                <p></p>
                <p>The infrastructure provisioned in this project includes among other AWS Aurora in multi-AZ mode and Vpn Client for
                secure connection to the private subnet where DB is deployed to.</p>
                <p>I wanted to check the current status of AWS Cloud integration in the Spring Cloud project. For that, I've
                implemented a simple starter project to test out database failover and integration with the AWS manager.
                The project can be found on Github:</p>
                <a href="https://github.com/stokilo/aws-spring-aurora-cluster" rel="noopener noreferrer" target="_blank">https://github.com/stokilo/aws-spring-aurora-cluster</a>
                <p></p>
              </div>


              <div class="mb-5">
                <h3 class="card-title">Spring properties</h3>
                <p>There are 3 main parts of the Spring application.properties file.</p>
                <p>First is app name and cloud.aws.* context setup. That is the standard setup required by the library.</p>
                <p>The second part consists of two data sources, one for the writer and one for the reader endpoint.
                  Credentials and jdbcUrl are fetched directly from the AWS Secret Manager. URL reader/writer.rds.com
                  is configured in a private hosted zone as part of infrastructure provisioning.
                </p>
                <p>The remaining configuration is for JPA and connection pool, in general, it is optional for this setup.</p>
                <p></p>
                <p>I've configured Spring Cloud 2.3.10.RELEASE with Spring boot starter.</p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet1"/>
                </client-only>
                <p></p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Secret management</h3>
                <p>Infrastructure provisioned with CDK includes RDS generated with a new secret with name <b>/config/aws-spring-aurora-cluster</b></p>
                <p>In order to fetch this secret, I'm passing a configuration in bootstrap.properties to change the secret prefix, I change it from
                /application to /config</p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet2"/>
                </client-only>
                <p>
                  I didn't spend much time on secret configuration. I had some problems with it. In order to make it work
                  you need to include dependency to <b>spring-cloud-starter-aws-secrets-manager-config</b> in the pom.xml.
                  This is enough for Spring Cloud to make a web service call to AWS and fetch secrets from two scopes,
                  application and global. More details of what the secret name should be can be found in the documentation.
                  My issue with this approach was that, in contrast to the AWS Parameter Store, I was not able to find a way
                  to define more secrets. It worked ok for database secret but I still don't know how to use more than
                  two secrets in the application. It looks like Spring expects I keep all my secrets in a single instance
                  of the secret. In my case I provision stack with CDK and database secret is a special construct
                  that is required by RDS, I can't modify it and include more data, and that is probably not ok to do it this way.
                </p>
                <p>
                </p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Read replica</h3>
                <p>The main feature of Aurora RDS in multi-AZ mode is HA.</p>
                <p>
                  I've configured two data sources in the spring context. One for the writer and one for the reader.
                  Additionally, I've created two transaction managers associated with data sources.
                </p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet3"/>
                </client-only>
                <p></p>
                <p>Here it is important to notice that reader.rds.com and writer.rds.com are private hosted zone DNS CNAME entries.
                Vpn connection is required to test this setup locally because RDS has public access disabled.
                  Additionally, for the failover scenario, please notice we depend on Java DNS caching.
                </p>
                <p></p>
                <p>Unfortunately, I could not configure the Aurora cluster in the tested Spring Cloud version.
                The cluster configuration is not supported, it will be included in 3.0.x version.</p>
                <a href="https://github.com/spring-cloud/spring-cloud-aws/issues/356" rel="noopener noreferrer" target="_blank">https://github.com/spring-cloud/spring-cloud-aws/issues/356</a>
                <p></p>
                <p>Suggested solutions are described in the following blogs:</p>

                  <a href="https://vladmihalcea.com/read-write-read-only-transaction-routing-spring/" rel="noopener noreferrer" target="_blank">https://vladmihalcea.com/read-write-read-only-transaction-routing-spring/</a>
                <p></p>
                  <a href="https://fable.sh/blog/splitting-read-and-write-operations-in-spring-boot/" rel="noopener noreferrer" target="_blank">https://fable.sh/blog/splitting-read-and-write-operations-in-spring-boot/</a>
                <p></p>

                <p>
                  These solutions are not implemented in this project, I've implemented a simple failover handler class that
                  monitors writer endpoint errors. In such cases, the connection pool is evicted.
                  This project configures two data sources, one for the writer and one for the reader endpoint.
                </p>
                <p></p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet4"/>
                </client-only>
                <p>
                  Spring Cloud is using an approach to annotate read-only service functions with @Transactional(readOnly=true)
                  annotation. Because of mentioned limitations of Spring Cloud, I've decided to implement a different approach.
                  I annotate read only service functions, that I want to route over
                  read replica, with a value of TransactionalOverReadReplica.READ_REPLICA. This will route them via
                  transaction manager associated with the read replica.
                </p>
                <p></p>
                <p>This configuration results in the distribution of read/writes over writer and reader nodes.
                The picture on top of the page is an example of this behavior. Testing instructions
                are included on github README.MD</p>
              </div>

              <div class="mb-5">
                <h3 class="card-title">Failover</h3>
                <p>Failover testing can be performed directly from the AWS Console. You can also use SDK API
                to run failover action.</p>
                <p>I've decided to run multiple read/write transactions and execute failover in between. As result, I get a database
                connection errors.</p>
                <p>As mentioned before, I could not use Spring Cloud for my setup. Spring Cloud support failover retry scenario.
                In my case, I've decided to implement a simply exception handler in form of the Spring aspect.</p>
                <p></p>
                <p>I've implemented catchDbQueryException function to detect Postgres specific error with code 25006.</p>
                <p>This is an error that is thrown in case the writer become read replica and pending connection pool
                connection attempts to execute write queries.</p>
                <p></p>
                <client-only>
                  <highlightjs langugage="python" :code="snippet5"/>
                </client-only>
                <p>
                  Imagine the following scenario, AZA with the writer instance and AZB with the reader. When you execute failover, the role of
                  these db instances is switched. This can be observed almost immediately after running failover from
                  the console because this is not real world testcase. In a real scenario, there would be a delay.
                  Now, the reader becomes a writer and a writer a reader. Endpoint DNS name stays that same, only IP behind the
                  DNS CNAME is updated. This is a problem when the connection pool still has pending connections. When
                  there are connections that attempt to execute write transactions, the transaction will fail with Postgres error 25006,
                  it is because they point now to the read replica.
                </p>
                <p>
                  I evict all connections from the read/write connection pools when this exception is thrown.
                  In an effect, there is a short time window when transactions fail, but the system resumes after 20-30 seconds.
                </p>
                <p>
                  One side effect for read transactions with this approach is not handled in the project. It is possible that after failover, read replica
                  is not used anymore and all queries go over the writer. This is because we still have pending
                  connections in the pool and reader DNS CNAME is cached by Java. The connection pool manager is not checking
                  DNS resolution and we end up with unused read replica instances.

                </p>
                <p>
                  Why is it working for the writer data source after failover? Because we listen on the error and when a pool
                  is evicted, it is possible that DNS caching still applies to the reader endpoint (reader.rds.com).
                  After the writer pool is evicted we don't get errors anymore, reader pool remains as it was before
                  failover, thus it is possible that talk with the writer node.
                </p>
                <p>
                  One solution I can think of is to monitor reader.rds.com IP and evict the connection pool when change
                  is detected. Such a task could run i.e. every minute to keep recovery time as short as possible.
                </p>
                <p>
                  I think that is probably worth investigating a solution with checking AWS database events using SDK.
                  When the writer node is changed we could do the same connection pool eviction as in the case of updated IP.
                </p>

              </div>


              <div class="mb-5">
                <h3 class="card-title">Failover with AWS PostgresSQL JDBC driver</h3>
                <p>I found out new, initial release of AWS PostrgresSQL JDBC driver, it supports failover for Aurora cluster</p>
                <p>More details can be found here:</p>
                <a href="https://github.com/awslabs/aws-postgresql-jdbc" rel="noopener noreferrer" target="_blank">https://github.com/awslabs/aws-postgresql-jdbc</a>
                <p></p>
                <p>This is a new driver released week ago. It supports custom domain name for JDBC URL but it didn't work for me after failover,
                  my connections were terminated. However, setting cluster reader/writer endpoint DNS name worked. I configured
                  two data sources, reader and writer, failover worked for both same way as for my custom PostgresFailoverAspect
                  implementation.</p>
                <p>This driver is enabled by default in the sample project. To switch to PostgresFailoverAspect, check its code, plus pom.xml and application.properties must be updated.</p>
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
    title: 'AWS CDK Aurora and Spring Cloud',
    meta: [
      {
        hid: 'description',
        name: 'description',
        content: 'AWS CDK RDS Aurora and Spring Cloud'
      },
      {
        hid: 'keywords',
        name: 'keywords',
        content: 'aws, cdk, aurora, rds, spring, spring cloud, Postgres, JDBC'
      }
    ]
  }
})
export default class AwsAuroraSpringCloud extends Vue {

  snippet1: String = `
spring.application.name=aws-spring-aurora-cluster
server.port=8081

cloud.aws.credentials.profile-name=default
cloud.aws.region.auto=false
cloud.aws.region.static=me-south-1
cloud.aws.stack.auto=false

datasource.writer.password=\${password}
datasource.writer.username=\${username}
datasource.writer.driverClassName=org.postgresql.Driver
datasource.writer.jdbc-url=jdbc:postgresql://writer.rds.com:\${port}/\${dbname}

datasource.reader.password=\${password}
datasource.reader.username=\${username}
datasource.reader.driverClassName=org.postgresql.Driver
datasource.reader.jdbc-url=jdbc:postgresql://reader.rds.com:\${port}/\${dbname}

spring.jpa.hibernate.ddl-auto=update
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.show-sql=true

spring.datasource.hikari.connectionTimeout=7000
spring.datasource.hikari.idleTimeout=10000
spring.datasource.hikari.maxLifetime=30000
  `

  snippet2: String = `
aws.secretsmanager.prefix=/config
  `

  snippet3: String =
    `
package com.sstec.spring.aurora.config;


import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;

@Configuration
public class DataSourceConfig {

    @Bean(name="writer.rds.com")
    @Primary
    @ConfigurationProperties(prefix="datasource.writer")
    public DataSource getWriterDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean(name="reader.rds.com")
    @ConfigurationProperties(prefix="datasource.reader")
    public DataSource getReaderDataSource() {
        return DataSourceBuilder.create().build();
    }


    @Bean(name="transactionManager")
    @Autowired
    @Primary
    DataSourceTransactionManager getWriterTransactionManager(@Qualifier ("writer.rds.com") DataSource writerDataSource) {
        return new DataSourceTransactionManager(writerDataSource);
    }

    @Bean(name=TransactionalOverReadReplica.READ_REPLICA)
    @Autowired
    DataSourceTransactionManager getReaderTransactionManager(@Qualifier ("reader.rds.com") DataSource readerDataSource) {
        return new DataSourceTransactionManager(readerDataSource);
    }
}

  `
  snippet4: String =
  `
@Service
public class UserService {

    UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public void createRandomUser() {
        User user = new User();
        user.setName(String.format("test-user-%s", System.currentTimeMillis()));
        user.setEmail("test-email@email.com");
        user.setCreationDate(LocalDateTime.now());
        userRepository.save(user);
    }

    @Transactional(value = TransactionalOverReadReplica.READ_REPLICA)
    public List<User> fetchLastCreated() {
        return userRepository.findTop10ByOrderByCreationDateDesc();
    }

}
  `

  snippet5: String =
    `
package com.sstec.spring.aurora.config;

import com.zaxxer.hikari.HikariDataSource;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.hibernate.exception.GenericJDBCException;
import org.postgresql.util.PSQLException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.orm.jpa.JpaSystemException;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;

/**
 * Failover support for Aurora Postgres multi AZ setup. Evict SQL connection from the pool on postgres error code: 25006
 * (read_only_sql_transaction).
 * Reader and writer endpoints can be a victim of DNS caching in failover scenario. Connections pointing to the
 * writer instance can be exchanged with reader one and that will causes error for each following write query.
 *
 * Relying on DNS cache eviction didn't work for me, AWS documentation:
 * https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.BestPractices.html
 *
 * In case of AZ failure this should be done anyway.
 */
@Aspect
@Component
public class PostgresFailoverAspect {

    //https://www.postgresql.org/docs/9.4/errcodes-appendix.html
    private static final String SQL_STATE_READ_ONLY_SQL_TRANSACTION = "25006";

    Logger logger = LoggerFactory.getLogger(PostgresFailoverAspect.class);

    @Qualifier("writer.rds.com")
    @Autowired
    private DataSource writerDataSource;

    @Qualifier("reader.rds.com")
    @Autowired
    private DataSource readerDataSource;

    @AfterThrowing(pointcut = "within(com.sstec.spring.aurora..*)", throwing = "exception")
    public void catchDbQueryException(Exception exception) {
        if (exception.getClass() == JpaSystemException.class) {
            Throwable causeLevel1 = exception.getCause();
            if (causeLevel1.getClass() == GenericJDBCException.class) {
                Throwable causeLevel2 = causeLevel1.getCause();
                PSQLException psqlException = (PSQLException) causeLevel2;

                if (psqlException.getSQLState().equals(PostgresFailoverAspect.SQL_STATE_READ_ONLY_SQL_TRANSACTION)) {
                    softEvictConnections(writerDataSource);
                    softEvictConnections(readerDataSource);
                }
            }
        }
    }

    private void softEvictConnections(DataSource dataSource) {
        try {
            ((HikariDataSource) (dataSource)).getHikariPoolMXBean().softEvictConnections();
            logger.debug("Called softEvictConnections() on the data source");
        } catch (Exception exception) {
            logger.error("Failed to evict connections from the pool", exception);
        }
    }
}

    `
}
</script>

