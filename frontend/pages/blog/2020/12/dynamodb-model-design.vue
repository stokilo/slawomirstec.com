<template>
  <b-tabs nav-class="separator-tabs ml-0 mb-5" content-class="tab-content" :no-fade="true">
    <b-tab title="DynamoDb dashboard model design">
      <div>
        <b-row>
          <b-card class="mb-4" no-body>
            <b-card-body>
              <div class="mb-5">
                <h3 class="card-title">Dashboard</h3>
                <p>
                  The application dashboard is a default view presented to the user after login. It consists of two parts:
                </p>
                <ol>
                  <li>Sum of all contacts/users/to-do items in the system</li>
                  <li>Audit events for all users, the newest on the top</li>
                </ol>
                <p></p>
                <p>
                  I decided to implement this to test out the DynamoDb model design and PynamoDB library. So let's begin with the PynamoDB.
                </p>
              </div>
              <hr/>
              <div class="mb-5">
                <h3 class="card-title">PynamoDB</h3>
                <p>
                  <a href="https://pynamodb.readthedocs.io/en/latest/">PynamoDB</a> is a python abstraction over DynamoDB API.
                </p>
                <p>
                  In the official AWS Python documentation, you can find sample code using the boto3 library.
                  Boto3 is the AWS SDK for Python.
                  For example, to query a table like 'Movies', you need to execute code similar to the one below:
                </p>
                <client-only>
                   <highlightjs language='python' :code="snippet1"/>
                </client-only>
                <p>
                  From what I have learnt, ORM solutions for DynamoDB are not recommended.
                  It would be best if you used direct SDK API calls.
                  I found a similar comment about ORM in the Alex DeBrie book:
                </p>
                <a href="https://www.dynamodbbook.com/">https://www.dynamodbbook.com/</a>
                <p></p>
                <p>
                  I think the correct approach is to avoid additional levels of abstraction for DynamoDb interactions.
                  It is a repetitive task to maintain mappings, using string placeholders and different expressions/key
                  definitions for every query. This type of code can quickly inflate the codebase which encourages you
                  to copy & paste between files. But there are also benefits. For example,
                  I find syntax very expressive and easy to use.
                </p>
                <p></p>
                <p>
                  Designing a DynamoDb data model can be challenging for developers that are only
                  familiar with the relational database. This approach allows beginners to focus on the
                  design problem and not on the syntax.
                </p>
                <p></p>
                <p>
                  However, I did not use the boto3 library in the sample application. PynamoDB is not an ORM; it is an
                  intermediate interface between your code and DynamoDB API. I found it easy to use, and the
                  documentation is short and concise. So I decided to give it a try.
                </p>
                <p>
                  You can find samples in the official documentation of PynamoDB. For the application dashboard,
                  I defined two PynamoDb models. I'm using a single table design for DynamoDB, which means I must
                  use a single table for all the application data I store. I design PK (partitions key)/SK (sort key)
                  so that entities share the same prefix. I use prefixes like table names in relational databases.
                  The prefix is used with the # sign to express the parent -> child relationship.
                </p>
                <p>
                  Returning to the entity models, the first table stores the count of contacts/users/to-do items.
                  Only one row in the application table is needed for this data. The count is updated in services
                  responsible for the creation of the entities. I model this entity with a singleton entity for
                  which partition key (PK) is: <strong>DASHBOARD#DASHBOARD_STATS#</strong>
                  and sort key (SK) is equal to PK: <strong>DASHBOARD#DASHBOARD_STATS#</strong>
                </p>
                <client-only>
                   <highlightjs langugage="python" :code="snippet2"/>
                </client-only>
                <p></p>
                <p>
                  Some of the classes in the examples are part of my API, i.e., BaseSingletonEntityForPyAwsV1.
                  They don't belong to the PynamoDb; please ignore them. In short, in a single table design,
                  sharing the PK and SK prefix is quite common. This is why you don't see PK/SK declarations in the
                  <strong>DashboardStats</strong> model.
                  I do this in the parent class by default, and the child only defines the prefix.
                </p>
                <p>
                  Second model stores audit events (actions executed by users). Every time entities are created,
                  I save one audit event. Besides the required keys, the audit event has the type and creation date.
                  In this case, I define the model prefix, but in the constructor, I set different SK. I need to
                  do this because it is not a singleton. Please ignore GSI setters. They are not used in this example.
                </p>
                <client-only>
                   <highlightjs langugage="python" :code="snippet3"/>
                </client-only>
                <p></p>
                <p>
                  In conclusion, the PK (partition key) value is equal to <strong>DASHBOARD#DASHBOARD_STATS#</strong>.
                  for both models. SK has two formats for the value:
                </p>
                <ul>
                  <li>For singleton: SK = PK = <strong>DASHBOARD#DASHBOARD_STATS#</strong></li>
                  <li>For one-to-many relation: SK = <strong>#DASHBOARD#DASHBOARD_STATS#{unique-item-id}</strong></li>
                </ul>
                <p>
                  The prefix for log item SK is slightly different. There is an additional hash in front of the key.
                  This is because we have one access pattern in the sample application:
                </p>

                <p>
                  Return statistics <strong>AND</strong> latest audit events in <strong>single</strong> DynamoDb query
                  request.
                </p>

                <p>
                  It is essential to do this in a single call. You don't want to fetch them separately because it will cost more
                  read capacity units.
                </p>
                <p>
                  How this is realized, and why additional # is required for audit event SK?
                </p>
                <p>
                  In the query result,
                  we want to get the first record for statistics (singleton)
                  followed by a list of the newest audit log events. Because we want to get the latest one, we must
                  add an additional # to audit event SK that they appear before singleton. Prepending # to the SK changes
                  the order of the items in the index to make our access pattern possible.
                  DynamoDB query must scan the index backward to get the latest entries. Please check the screenshot.
                  A backward scan will start returning entries starting from statistics singleton. Then the latest
                  added audit events, that is why # is appended to SK.
                </p>
                <ResizeImageTag resizeTo=1200 src="blog/2020/12/db-dashboard.jpg"
                                class-name="responsive border-0 card-img-top mb-3" alt="DynamoDb Dashboard"/>
                <p></p>
                <p>
                  In PynamoDB, the query with the backward scan is defined by a parameter:
                  <strong>scan_index_forward=False</strong>.
                  Additionally, we must limit the number of rows to 10.
                  To return combined data from singleton and audit events, I defined a new model with projection columns
                  for both of them. DynamoDB query is straightforward; it relies on the ordering and value of the
                  PK/SK items. Because we are using a single table design, our keys are unique and defined for
                  each entity, and we can be sure that <strong>DASHBOARD#DASHBOARD_STATS#</strong>
                  represents an entity with dashboard a) stats b) audit events. In our case, the PK/SK combination
                  plus explicit sort order (#SK prefix) ensures that in the response, we will get following columns with not null fields:
                </p>
                <client-only>
                <ul>
                  <li>
                    Statistics fields contact count/user count/todo count.
                  </li>
                  <li>
                    Audit Event type/creation_date.
                  </li>
                </ul>
                </client-only>
                <p></p>
                <client-only>
                   <highlightjs langugage="python" :code="snippet4"/>
                </client-only>

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
  title: 'AWS DynamoDb model design',
    meta: [
    {hid: 'description', name: 'description', content: 'Description of DynamoDb model design'},
    {hid: 'keywords', name: 'keywords', content: 'AWS, DynamoDB, PynamoDb, Boto3, CDK, GSI, SK, PK, Python, backend' }
  ]
}
})
export default class PiafDesign extends Vue {
  snippet1: String = `
from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key


def query_and_project_movies(year, title_range, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')
    print(f"Get year, title, genres, and lead actor")

    # Expression attribute names can only reference items in the projection expression.
    response = table.query(
        ProjectionExpression="#yr, title, info.genres, info.actors[0]",
        ExpressionAttributeNames={"#yr": "year"},
        KeyConditionExpression=
            Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
    )
    return response['Items']
  `
  snippet2: String = `
class DashboardStats(BaseSingletonEntityForPyAwsV1):
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    contactCount = NumberAttribute(default=0, null=False)
    userCount = NumberAttribute(default=0, null=False)
    todoCount = NumberAttribute(default=0, null=False)
    last_change_date = UTCDateTimeAttribute()

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.last_change_date = datetime.utcnow()

    def prefix(self) -> str:
        return "DASHBOARD#DASHBOARD_STATS#"
  `

  snippet3: String = `
class DashboardAuditLogItemEntity(BaseEntityForPyAwsV1):
    """Entity for dashboard audit log items
    """
    class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    def __init__(self, unique_id: str = "", **kwarg):
        super().__init__(unique_id, **kwarg)
        # Shared pk with DashboardStats entity, different sort key, we want to fetch them both in single call
        self.pk = self.get_pk("")
        self.sk = self.get_sk(unique_id)
        self.gsi1pk = self.get_pk("")
        self.gsi1sk = self.get_sk(unique_id)

    type = UnicodeAttribute(null=False)
    creation_date = UTCDateTimeAttribute(null=False)


    def get_sk(self, unique_id: str):
        # ## because of sort order
        return f"#{self.prefix()}{unique_id}"

    def prefix(self) -> str:
        return "DASHBOARD#DASHBOARD_STATS#"
  `

  snippet4: String = `

class DashboardStatsAndLogsView(Model):
     class Meta(BaseEntityForPyAwsV1.Meta):
        initialized = True

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    gsi1pk = UnicodeAttribute()
    gsi1sk = UnicodeAttribute()
    contactCount = NumberAttribute(default=0, null=False)
    userCount = NumberAttribute(default=0, null=False)
    todoCount = NumberAttribute(default=0, null=False)
    last_change_date = UTCDateTimeAttribute()
    type = UnicodeAttribute(null=False)
    creation_date = UTCDateTimeAttribute(null=False)

    def prefix(self) -> str:
        return "DASHBOARD#DASHBOARD_STATS#"


class DashboardDao(BaseDao[DashboardStats]):

    def get_dashboard(self) -> List[DashboardStatsAndLogsView]:
        items = []
        dashboard_view = DashboardStatsAndLogsView()
        dashboard_view.pk = dashboard_view.prefix()
        item_iterator = DashboardStatsAndLogsView.query(dashboard_view.pk, limit=10, scan_index_forward=False)
        for item in item_iterator:
            items.append(item)
        return items
  `
}
</script>

