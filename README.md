# json-ws-test


## License

Copyright (c) 2013-2014 Ujjawal Misra. See the LICENSE file for license rights and limitations (MIT).


## Description

**JSON** (JavaScript Object Notation) is being heavily used in various projects, systems and platforms as the response format of **web-services**. The web-services may, themselves, be RESTful or using HTTP Methods like GET or POST for making a call, i.e. for passing inputs. 

Developers end-up writing and saving curl calls for testing these web-services as and when they develop or change them. This is really ugly and cumbersome (to keep modifying these 'saved' curl calls for repetitive testing) !! Plus such a mechanism disallows using these curl calls to be seamlessly integrated in a Test-Suite or a Nightly-Build Test System, etc.

**json-ws-test** is simple framework for testing **JSON (response) Web-Services**. 

The Test-Cases, i.e. the ugly curl calls you were having earlier, are written in a JSON file using a simple and flexible format defined by the json-ws-test framework. This test-cases JSON file is passed as an argument to the framework, which then executes these test-cases and generates a SUMMARY for them in a Tabular as well as JSON structure.


### Sample

For the purpose of letting you have a flavor of what is in store for you in this framework we will use http://jsontest.com -- an online platform that exposes various web-services generating JSON responses.

Consider the following sample test-case written in the JSON structure defined by json-ws-test framework:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "Echo",
            "host" : "http://echo.jsontest.com/key/value/one/two",
            "output" : {
                "params" : [
                    {
                        "check" : "EXACT",
                        "name" : "key",
                        "expected" : "value"
                    },
                    {
                        "check" : "EXACT",
                        "name" : "one",
                        "expected" : "two"
                    }
                ]
            } 
        }
    ]
}
```


It is using a RESTful web-service (refer 'host') that returns the following JSON response:

```js
{
   "one": "two",
   "key": "value"
}
```

You can write the sample test-case in some file (you can find it in *sample/single.test.json*. You can then run the test-case from the base directory of the project as follows:

```bash
python src/Tester.py sample/single.test.json
```

Try it now!

You will see a JSON version of this Summary of the test-case execution in the logs generated on your terminal:

```
2013-10-30 18:19:47,781 - INFO     - Tester     - ================================
2013-10-30 18:19:47,781 - INFO     - Tester     - [SUMMARY JSON]
2013-10-30 18:19:47,781 - INFO     - Tester     - {'failed': {'count': 0, 'time': 0}, 'total': {'count': 1, 'time': 0.565485954284668}, 'steps': {'Echo': {'failed': {'count': 0, 'time': 0}, 'total': {'count': 1, 'time': 0.565485954284668}, 'passed': {'count': 1, 'time': 0.565485954284668}}}, 'passed': {'count': 1, 'time': 0.565485954284668}}
2013-10-30 18:19:47,781 - INFO     - Tester     - ================================
```

You will also see a beautiful Summary in a tabular form for immediate use:

```
2013-10-30 18:19:47,781 - INFO     - Tester     - ================================
2013-10-30 18:19:47,781 - INFO     - Tester     - [SUMMARY]
2013-10-30 18:19:47,782 - INFO     - Tester     - |------------------------------|--------------|--------------|--------------|
2013-10-30 18:19:47,782 - INFO     - Tester     - |            [sid]             |   [total]    |   [passed]   |   [failed]   |
2013-10-30 18:19:47,782 - INFO     - Tester     - |------------------------------|--------------|--------------|--------------|
2013-10-30 18:19:47,782 - INFO     - Tester     - |                              | count avg(ms)| count avg(ms)| count avg(ms)|
2013-10-30 18:19:47,782 - INFO     - Tester     - |------------------------------|--------------|--------------|--------------|
2013-10-30 18:19:47,782 - INFO     - Tester     - |Echo                          |     1     565|     1     565|     0       0|
2013-10-30 18:19:47,783 - INFO     - Tester     - |------------------------------|--------------|--------------|--------------|
2013-10-30 18:19:47,783 - INFO     - Tester     - |OVERALL                       |     1     565|     1     565|     0       0|
2013-10-30 18:19:47,783 - INFO     - Tester     - |------------------------------|--------------|--------------|--------------|
2013-10-30 18:19:47,783 - INFO     - Tester     - ================================
```


## The Language Elements

Lets know do a walkthrough of the elements of the test-case definition language of this framework. All the elements are defined in JSON format.

### steps

The **steps** element is a JSON array that defines the order in which individual test-cases need to be executed. For example, in the following test-case JSON:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "Test-Case-1",
            ...
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-2",
            ...
        },
        ...
        {
            "construct" : "TEST",
            "sid" : "Test-Case-k",
            ...
        }
    ]
}
```

the test-cases will be executed in the specified order - Test-Case-1 followed by Test-Case-2 and so on uptil Test-Case-k.

### construct

The **construct** element is used to define a step in the execution of a flow to be tested.

#### [construct] TEST

The **TEST construct** is the actual evaluation or processing step that leads to a web-service being called. For example, in the following test-case JSON:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "Echo",
            "host" : "http://echo.jsontest.com",
            "path" : "/key/value/one/two",
            "method" : "GET",
            "input" : {
                ...
            }, 
            "output" : {
                ...
            } 
        }
    ]
}
```

* "construct" : "TEST" -- [required] -- specifies the construct type.
* "sid" : "Echo" -- specifies the step-id. This is of particular importance as we will see in case of *construct START_SESSION and END_SESSION*.
* "host" : "http://echo.jsontest.com" -- [required] -- specifies the web-service to be hit.
* "path" : "/key/value/one/two" -- [optional, default is ""] -- specifies the path to be appended to the *host*. Alternatively, the *host* may be fully qualified with the path (eg. "host" : "http://echo.jsontest.com/key/value/one/two") in which case this attribute may be omitted.
* "method" : "GET" -- [optional, default is "GET"] -- specifies the HTTP-method to be used for hitting the web-services.
* "input" : { .. } -- [optional, default is {}] -- specifies the arguments to be passed to the web-service.
* "output" : { .. } -- [optional, default is {}] -- specifies the criteria for validation of the output of the web-service. Refer **check** section for further details.

#### [construct] START_LOOP

#### [construct] END_LOOP

#### [construct] START_SESSION

#### [construct] END_SESSION

#### Input/Output

### Default

### check

#### [check] PRESENT

#### [check] EXACT


