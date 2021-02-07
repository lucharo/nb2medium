Summary of the things I learn while writing this package

# Medium API

## Where can I get a Medium API token?

To get a token for your Medium account you will need to go to: __Settings > Integration tokens__, then create a new integration token. You can give your token any name but I propose using something like `nb2medium`.

If this option is not available by default you may need to:
> Users can request an access token by emailing yourfriends@medium.com. We will then grant access on the Settings page of their Medium account.

## Where can I read the Medium API documentation?

[Medium's Github](https://github.com/Medium/medium-api-docs)

## What is REST API?

From [stackify.com](https://stackify.com/rest-api-tutorial/):
> Even though REpresentational State Transfer, also known as REST, is often referred to as a protocol, it’s an architectural style. It defines how applications communicate over the Hypertext Transfer Protocol (HTTP). Applications that use REST are loosely-coupled and transfer information quickly and efficiently. While REST doesn’t define data formats, it’s usually associated with exchanging JSON or XML documents between a client and a server.

## How to authenticate to Medium API from command line

First of all the access/integration token needs to be used for all communications. Now, how do we pass the token to the server?
```sh
curl -s -H "Authorization: Bearer $MEDIUM_TOKEN" https://api.medium.com/v1/me 
```
This command will return info about the user (yourself if you're not malicious) as a JSON.

`MEDIUM_TOKEN` in this case is an environment variable stored in my computer.

curl docs for these options:
```
-s, --silent
      Silent or quiet mode. Don't show progress meter or error messages.  Makes Curl mute. It will still output the data you
      ask for, potentially even to the terminal/stdout unless you redirect it.

      Use -S, --show-error in addition to this option to disable progress meter but still show error messages.

      See also -v, --verbose and --stderr.
-H, --header <header/@file>
              (HTTP) Extra header to include in the request when sending HTTP to a server. You may specify any number of extra head‐
              ers. Note that if you should add a custom header that has the same name as one of the internal ones  curl  would  use,
              your  externally set header will be used instead of the internal one. This allows you to make even trickier stuff than
              curl would normally do. You should not replace internally set headers without knowing perfectly well what  you're  do‐
              ing.  Remove  an  internal  header  by  giving a replacement without content on the right side of the colon, as in: -H
              "Host:". If you send the custom header with no-value then its header must be terminated with a semicolon, such  as  -H
              "X-Custom-Header;" to send "X-Custom-Header:".
```


Also, I think the [Medium documentation](https://github.com/Medium/medium-api-docs#31-users) does not clearly show how to do this (if you are like me with no Web experience)

### The command line thinks the output is just text and print its uglily? How can I pretty print?

Using [`jq`](https://ostechnix.com/how-to-parse-and-pretty-print-json-with-linux-commandline-tools/) and piping the `curl` stdout into it:
```bash
!curl -s -H "Authorization: Bearer $MEDIUM_TOKEN" https://api.medium.com/v1/me | jq
```


### How to get publications from your account?

In the Medium jargon, publications is more akin to an Editor or publisher, not an article by itself (e.g. Towards Data Science, Towards AI, JavaScript in English...)

```bash
!curl -H "Authorization: Bearer $MEDIUM_TOKEN" "https://api.medium.com/v1/users/$MEDIUM_USER_ID/publications" | jq
```

The Medium User ID can be retrieved from the first request, the one that fetches info about the user (the `id` entry).

### How to post an article via the API?

[Using the POST method:](https://github.com/Medium/medium-api-docs#33-posts)

```bash
!curl -X POST \
        -H "Authorization: Bearer $MEDIUM_TOKEN" \
        -d 'title=TestAPI&contentFormat=markdown&content=# I can post from the CLI&publishStatus=draft' \
        "https://api.medium.com/v1/users/$MEDIUM_USER_ID/posts" | jq
```

Which could also look like:
```bash
!curl -X POST \
        -H "Authorization: Bearer $MEDIUM_TOKEN" \
        -d 'title=TestAPI' \
	-d 'contentFormat=markdown' \
	-d 'content=# I can post from the CLI' \
	-d 'publishStatus=draft' \
        "https://api.medium.com/v1/users/$MEDIUM_USER_ID/posts" | jq
```

__`curl` documentation:__

-d, --data <data>
       (HTTP)  Sends the specified data in a POST request to the HTTP server, in the same way that a browser does when a user
       has filled in an HTML form and presses the submit button. This will cause curl to pass the data to  the  server  using
       the content-type application/x-www-form-urlencoded.  Compare to -F, --form.

       --data-raw  is  almost the same but does not have a special interpretation of the @ character. To post data purely bi‐
       nary, you should instead use the --data-binary option.  To URL-encode the value of a form field you may use --data-ur‐
       lencode.

       If  any of these options is used more than once on the same command line, the data pieces specified will be merged to‐
       gether with a separating &-symbol. Thus, using '-d name=daniel -d skill=lousy' would generate a post chunk that  looks
       like 'name=daniel&skill=lousy'.

       If  you  start the data with the letter @, the rest should be a file name to read the data from, or - if you want curl
       to read the data from stdin. Multiple files can also be specified. Posting data from a file named 'foobar' would  thus
       be done with -d, --data @foobar. When --data is told to read from a file like that, carriage returns and newlines will
       be stripped out. If you don't want the @ character to have a special interpretation use --data-raw instead.


__Note__, we can pass in a file's content by preceding it's path with `@`, for example:
If we have file `test.md` such that:
```md
# This is the title

## This is a subtitle

This is the main body, __bold__ words, _italic_ and ~deleted~.
```
a = 1
b = 2
c = a + b
```
```

The POST request would look like (as long as the `curl` call is in the same directory as `test.md`):
```bash
!curl -X POST \
        -H "Authorization: Bearer $MEDIUM_TOKEN" \
        -d 'title=TestAPI' \
        -d 'contentFormat=markdown' \
        --data-urlencode "content@test.md" \
        -d 'publishStatus=draft' \
        "https://api.medium.com/v1/users/$MEDIUM_USER_ID/posts" | jq
```

__All the possible options to specify are described in the [Medium API docs (Create a post section)](https://github.com/Medium/medium-api-docs#creating-a-post).__

Note also that there is no way to change what's uploaded other than connect to Medium via your web browser. That means, that if you re-upload a file with the same title a new article will be created and be given a unique idenitifier which can make the draft fox rather messy.

### Uploading images

Let's say we have an image, like GitHub's logo:
![](https://cdn.afterdawn.fi/v3/news/original/github-logo.png)

We can upload this from the CLI too:
```bash
!curl -X POST https://api.medium.com/v1/images \
	-H "Authorization: Bearer $MEDIUM_TOKEN" \
	-F 'name="image"; filename="github-logo.png" ; type="image/png";' \
	-F 'image=@github-logo.png' | jq
```

This outputs a JSON dictionary with the image's URL and an md5 identifier, which could be useful to store to avoid reuploading images to the Medium servers.

I also realised late that `GET` and `POST` are command line programs too but I find it harder to work with them than with cURL.
The uncomfortable thing about working with them (at least to upload images) is that that file image.txt(as per seen in the next ref) needs to have CRLF endings (like DOS files) as opposed to LF ending files (like Unix)[SO](https://stackoverflow.com/a/10765244/12821043). This is equivalent to all lines ending by `\r\n` in the form part.

## CURL conclusion

We've gotten quite far with cURL alone from the CLI but we can do the same and potentially in an easier way from python :)

# Jupyter Extensions

# Parsing a Jupyter notebook
