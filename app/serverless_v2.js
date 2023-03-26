const AWS = require('aws-sdk')

const dynamodb = new AWS.DynamoDB.DocumentClient()

exports.handler = async (event, context) => {
  let count = 0 // initial state
  const params = {
    TableName: 'count-state',
    Key: { id: 'current-count' }
  }

  try {
    const result = await dynamodb.get(params).promise()
    if (result.Item) {
      count = result.Item.count
    }
  } catch (error) {
    console.error('Failed to retrieve count state from DynamoDB', error)
  }

  if (event.httpMethod === 'GET') {
    return {
      statusCode: 200,
      body: `Current count: ${count}`
    }
  } else if (event.httpMethod === 'POST') {
    const operation = event.path === '/increment' ? 'incremented' : 'decremented'
    count += operation === 'incremented' ? 1 : -1

    try {
      const result = await dynamodb.put({
        TableName: 'count-state',
        Item: { id: 'current-count', count }
      }).promise()
    } catch (error) {
      console.error('Failed to update count state in DynamoDB', error)
    }

    return {
      statusCode: 200,
      body: `Count ${operation} to ${count}`
    }
  } else {
    return {
      statusCode: 405,
      body: 'Method not allowed'
    }
  }
}
