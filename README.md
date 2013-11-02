# json-ws-test

Tes your JSON (response) Web-Services using JSON.


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

The *summary* defines how many times was each test-case executed and how many times did it pass or fail. It also specifies the average time (ms) taken for these outcomes, i.e. total (or overall), passed and failed.

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

The **START_LOOP construct** is the starting point of a loop, such that you can define what all test-cases (*TEST construct*) to be repeated and how many times. For example, in the following test-case JSON:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "Test-Case-1",
            ...
        },
        {
            "construct" : "START_LOOP",
            "count" : 5
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-2",
            ...
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-3",
            ...
        },
        {
            "construct" : "END_LOOP"
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-4",
            ...
        }
    ]
}
```

* "count" : 5 -- [optional, default is 1] -- specifies the number of times the loop should be repeated.

Test-Case-2 and Test-Case-3 will be executed one after the other repeatedly for 5 times, i.e. as [Test-Case-2, Test-Case-3, Test-Case-2, Test-Case-3,... (5 times)]. Test-Case-1 and Test-Case-4 will be executed just once as they do not fall in the loop ended by *END_LOOP construct*.

**NOTE:** Nesting of loops is not allowed.

#### [construct] END_LOOP

The **END_LOOP construct** is the ending point of a loop. Refer example in the *START_LOOP construct* section.

#### [construct] START_SESSION

The **START_SESSION construct** is the starting point for defining a list of test-cases such that they form a part of a session. 

Lets first understand what is the meaning of a *session* here. When creating test-cases you may want to use the *input* or *output* attributes of one test-case for defining the *input* or *output* attributes of another test-case. In order to facilitate this there needs to be a block that defines a list of test-cases where *input* and *output* of any test-case can be referred in a subsequent test-case within the block.

For example, in the following test-case JSON:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "Test-Case-1",
            ...
        },
        {
            "construct" : "START_SESSION"
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-2",
            "host" : "http://ip.jsontest.com",
            "input" : {
            },
            "output" : {
                "params" : [
                    {
                        "check" : "PRESENT",
                        "name" : "ip"
                    }
                ]
            } 
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-3",
            "host" : "http://echo.jsontest.com/ip/$OUT[Test-Case-2][ip]",
            "output" : {
                "params" : [
                    {
                        "check" : "EXACT",
                        "name" : "ip",
                        "expected" : "$OUT[Test-Case-2][ip]"
                    }
                ]
            } 
        },
        {
            "construct" : "END_SESSION"
        },
        {
            "construct" : "TEST",
            "sid" : "Test-Case-4",
            ...
        }
    ]
}
```

Test-Case-3 is refering to the output of Test-Case-2 for defining its web-service call (in the *host* attribute) as well as defining the expected output (*$OUT[Test-Case-2][ip]*). Test-Case-1 and Test-Case-4 cannot be referred in the session as they do not fall in the block ended by *END_SESSION construct*.

Following attributes of a *TEST construct* can be templatized in such a way:
* host
* path
* input (value part of the attributes in input)
* output (value part of the attributes in output)

Refer **Input/Output** section for further details.


**NOTE:** Nesting of sessions is not allowed.

#### [construct] END_SESSION

The **END_SESSION construct** is the ending point of the test-case list to be considered for being a part of the session. Refer example in the *START_SESSION construct* section.

#### Input/Output

Following keywords are supported for referring session (defined by *START_LOOP and END_LOOP constructs*) parameters:
* IN : to refer to input attributes of a previous test-case in the session
* OUT : to refer to output (response JSON generated by the web-service call) of a previous test-case in the session

The syntax for refering to a session parameter is:
* $IN[sid][attribute]
* $OUT[sid][attribute]
where *sid* is step-id and attribute is a JSON attribute being referred.

Examples,
* $IN[RegisterUser][user.address.city]
* $OUT[FindIP][ip]

### Default

If you want to use some common attributes across your test-cases you can use the **default** element. Following are the supported attributes for default value definition in this element:
* host
* path
* method
* input - this will act as the base input for all the test-cases. In case a test-case also has its own input attribute, that input attribute will be merged over this default input to come up with a unified input to be used in the test-case. Thus, the input attribute of a test-case will, in a way, override any common properties between it and the default input.

### check

The **check** element allows you to do validations on the JSON response of the web-service calls made by your test-cases.

#### [check] PRESENT

The **PRESENT check** simply checks if the specified attribute is present in the output (JSON response) or not. For example, in the following test-case JSON:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "FindIP",
            "host" : "http://ip.jsontest.com",
            "input" : {
            },
            "output" : {
                "params" : [
                    {
                        "check" : "PRESENT",
                        "name" : "ip"
                    }
                ]
            } 
        }
    ]
}
```

the framework will check whether the output of the web-service call has an attribute *ip* or not. For the sake of clarity the output of the web-service call made in this test case is something like:

```js
{"ip": "8.8.8.8"}
```

where the ip will be the IP of your system.

#### [check] EXACT

The **EXACT check** checks if the specified attribute present in the output (JSON response) has the exact value as specified in the *expected* parameter or not. For example, in the following test-case JSON:

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "FetchHeaders",
            "host" : "http://ip.jsontest.com",
            "input" : {
            },
            "output" : {
                "params" : [
                    {
                        "check" : "EXACT",
                        "name" : "Host",
                        "expected" : "headers.jsontest.com"
                    }
                ]
            } 
        }
    ]
}
```

the framework will check whether the output of the web-service call has an attribute *Host* and it has the exact value *headers.jsontest.com* or not. For the sake of clarity the output of the web-service call made in this test case is something like:

```js
{
   "Accept-Language": "en-US,en;q=0.8",
   "Host": "headers.jsontest.com",
   "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
```

#### Doing checks on nested (complex) response values

Suppose you want to check whether the output (JSON response) of your test-case web-service call has an attribute *result* that contains an attribute *user* with *id* as *12345* and *address* with *city* as *Bangalore*, i.e. something like the following response:

```js
{
    "result" : {
        "user" : {
            "id" : "12345",
            "email" : "user.email@somedomain.com",
            "address" : {
                "city" : "Bangalore",
                "state" : "Karnataka",
                "country" : "India"
            }
        }
    }
}
```

you can write your checks in one of the following ways:

* The nested way

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "FindUser",
            "host" : "http://some.webservice",
            "path" : "/user/get"
            "input" : {
                "email" : "user.email@somedomain.com"
            },
            "output" : {
                "params" : [
                    {
                        "check" : "PRESENT",
                        "name" : "result",
                        "expected" : [
                            {
                                "check" : "PRESENT",
                                "name" : "user",
                                "expected" : [
                                    {
                                        "check" : "EXACT",
                                        "name" : "id",
                                        "expected" : "12345"
                                    },
                                    {
                                        "check" : "PRESENT",
                                        "name" : "address",
                                        "expected" : [
                                            {
                                                "check" : "EXACT",
                                                "name" : "city",
                                                "expected" : "Bangalore"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            } 
        }
    ]
}
```

* The linear way

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "FindUser",
            "host" : "http://some.webservice",
            "path" : "/user/get"
            "input" : {
                "email" : "user.email@somedomain.com"
            },
            "output" : {
                "params" : [
                    {
                        "check" : "EXACT",
                        "name" : "result.user.id",
                        "expected" : "12345"
                    },
                    {
                        "check" : "EXACT",
                        "name" : "result.user.address.city",
                        "expected" : "Bangalore"
                    }
                ]
            } 
        }
    ]
}
```

* The mixed way

```js
{
    "steps" : [
        {
            "construct" : "TEST",
            "sid" : "FindUser",
            "host" : "http://some.webservice",
            "path" : "/user/get"
            "input" : {
                "email" : "user.email@somedomain.com"
            },
            "output" : {
                "params" : [
                    {
                        "check" : "PRESENT",
                        "name" : "result.user",
                        "expected" : [
                            {
                                "check" : "EXACT",
                                "name" : "id",
                                "expected" : "12345"
                            },
                            {
                                "check" : "EXACT",
                                "name" : "address.city",
                                "expected" : "Bangalore"
                            }
                        ]
                    }
                ]
            } 
        }
    ]
}
```

Seems like the best of both world, doesn't it ?! Make your pick.
