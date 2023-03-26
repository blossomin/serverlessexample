exports.handler = async (event, context) => {
    let count = 0 // initial state
  
    if (event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        body: `Current count: ${count}`
      }
    } else if (event.httpMethod === 'POST') {
      const operation = event.path === '/increment' ? 'incremented' : 'decremented'
      count += operation === 'incremented' ? 1 : -1
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
  