## api gateway integration with lambda versions

- create a lambda function. Test it. 
- Under actions: Publish new version (version-1)
- update the code
- under actions: publish new version (version-2)
- test it.

### To create an alias for version 1 and 2

- under actions: Create alias
- give version 4, under weighted alias: give verion 1
- test it.

### To integrate with API Gateway
- Create REST API gw
- Create Method: Get
- for lambda: 'lambdafunctionName:${stageVariables.lambdaAlias}'
e.g 'helloworldversion:${stageVariables.lambdaAlias}'
- save it

- execute the below command by replacing the '${stageVariables.lambdaAlias}' with alias name: 'oldestNewest'
```
aws lambda add-permission \
--function-name "arn:aws:lambda:eu-central-1:619831221558:function:helloworldversion:oldestNewest" \
--source-arn "arn:aws:execute-api:eu-central-1:619831221558:uiosv8p7le/*/GET/" \
--principal apigateway.amazonaws.com \
--statement-id 110eeb7c-a38c-4c71-9747-aaab02d90259 \
--action lambda:InvokeFunction
```

- for stage variables, add Name: lambdaAlias, value: oldesNewest
