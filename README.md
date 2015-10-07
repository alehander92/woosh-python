#woosh-python

a result of an insomniac 20 hours marathon

a shell written in python **in ridiculously early stage**

defines its own `woo` language and uses a simple yaml based configuration

![img](http://i.imgur.com/zP4pEjS.png)

##done

* arrows keys support 
* command history support
* syntax highlighting (of the implemented woo syntax)
* syntax aware completion on tab (can show you columns with file / arg / function completions in the same time )
* a very basic woo interpreter (woo needs lambdas and method support to really take off for now)
* a native command dsl 
* working yaml config infrastructure (not all settings are implemented yet)
* prompt pattern configuration in yaml
* abillity to create your own themes (currently themes are mixed with the main .woosh.yaml file)

##todo

* continue developing woo
* add variable support
* implement lambda, method and fun definition support
* implement system command support 
* support the other settings in .woosh.yaml, add modularized theme support
* fix tab completion
* wrap existing common system commands with woo typed interface


##examples

config of prompt:

```yaml
prompt: 
  pattern: '{time}~{username}@ {branch} {pwd} '
  username: [white, bold]
  host:     green
  time:     blue
  branch:   red
  repo:     white
  pwd:      white
```


##goals

* fast prototyping
* experiment with ..
* config settings
* woo syntax
* data structures inter-command transfer

###name

it is supposed to be a prototype for a `go`/`elixir` version.

###license

MIT, 2015 Alexander Ivanov

