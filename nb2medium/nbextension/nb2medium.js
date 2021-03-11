// A Jupyter notebook extension for Jupytext
// Refer to the documentation at
// https://github.com/mwouts/jupytext/blob/master/jupytext/nbextension/README.md

// The most convenient way to edit this file is to edit the version installed by pip at
// share/jupyter/nbextensions/jupytext

define([
    'jquery',
    'base/js/namespace',
    'base/js/dialog',
    'base/js/events',
    'base/js/utils',
    'base/js/i18n'
], function (
    $,
    Jupyter,
    dialog,
    events,
    utils,
    i18n
) {
    "use strict";
    
    
    var articleSubmitDialog = function () {
        // to learn how to write a Jupyter notebook extension
        // dialog, check the dialog.modal source code at https://github.com/jupyter/notebook/blob/bc28d6123117c3c733697e27e9d4bd71d7f0c46b/notebook/static/base/js/dialog.js
        // and google jquery help
        var articleTitleInputBox = $('<input>')
            .attr('type', 'text')
            .attr('placeholder', "Enter your article's title")
            .addClass('txt-articletitle')
                
        var submitArticle = $('<button>')
            .attr('type', 'button')
            .addClass('btn-submitarticle')
            .append('Submit')
        

        var submittedArticle = $('<span>')
            .attr('id', 'submitted-title')
        
        // the thing below is called event delegation in 
        // dynamically generated elements
        // read more at 
        // https://stackoverflow.com/questions/203198/event-binding-on-dynamically-created-elements
        $(document).on(
            'click', '.btn-submitarticle',
            function(){
                var articleTitle = $(".txt-articletitle").val();
                var isDebug = $('#debugFlag').prop('checked')
                console.log('[nb2medium] Article submitted as :'+articleTitle)
                // could add a spinner here
                pythonSubmitArticleScript(articleTitle,
                                          Jupyter.notebook.notebook_name,
                                          isDebug ? 'debug' : 'info')
            }
        )
        

        
        var debugCheckbox = $('<input>')
            .attr('type', 'checkbox')
            .attr('id', 'debugFlag')
        
        
        $(document).on(
            'change', '#debugFlag',
            function() {
                var currState = $('#debugFlag').prop('checked');
                $('#debugFlag').attr('checked', !currState)
                console.log('[nb2medium] Debug flag set to: ' + currState)
            }
        );
                
        var pythonOutput = $('<div>')
            .attr('id','nb2medium-output-container')
            .append(
                $('<div>')
                .addClass('row list_header')
                .append(
                    $('<span>')
                    .attr('id','nb2medium-output')
                )
            );
        
        var dialogform = $('<div/>')
            .attr('title', i18n.msg._('Submit notebook to Medium'))
            .addClass('dialogform')
            .append('Provide a title for your article and submit as a draft')
            .append('<br />')
            .append(articleTitleInputBox)
            .append(submitArticle)
            .append($('<div>')
                    .append(debugCheckbox)
                    .append(' Submit in <strong>debug mode</strong>')
            )
            .append(pythonOutput)
            //.append($('<div>')
            //      .append('Executing')
           

        dialog.modal({
            title: 'Upload notebook as Medium draft',
            body: dialogform,
            position: 'center',
            buttons: {Cancel: {}},  
            // the keyboard manager argument is passed
            // so that the dialog is aware of keybindings
            // otheriwse for e.g. pressing f in dialog mode would
            // trigger the find+replace dialog, etc...
            keyboard_manager: Jupyter.notebook.keyboard_manager
        })
 
    
    }
    
    
    // I believe the Jupyter JS api stops taking values after the first stderr 
    // stream comes in, even if the python keeps executuing, run python command
    // outputting data, data.content to check this. And unfortunately the logging 
    // output is seen as stderr
    const pythonPromise = function(python) {
        return new Promise((resolve, reject) => {
            var callbacks = {
                iopub: {
                    output: (data) => {
                        if (data.msg_type == "error") {
                            err = data.content.ename + ': ' +
                            data.content.evalue +' Traceback:' + data.content.traceback[0]
                            reject($('#nb2medium-output').text(err))
                        }
                        else if (data.msg_type == 'stream') {
                            // output from python print
                            resolve(data.content.text)
                        } else {
                            reject(
                                alert("nb2medium was not ready for this, please raise an issue with your setup")
                            )
                        }
                    } 
                }
            };

            Jupyter.notebook.kernel.execute(python, callbacks);    
        });
    }

    const pythonExecute = async(python, log_mode) => {
        let pythonResult = await pythonPromise(python);
        // here pythonResult is a variable I can manipulate
        // e.g. pythonResult.toUpperCase();
        // do smth here
        $('#nb2medium-output').html(pythonResult)
        console.log(pythonResult)
    }
        

   var pythonSubmitArticleScript = function(nbTitle, nbName, logLevel){
       let pycommand = pythonExecute(`
from nb2medium.upload import nb2medium
from io import StringIO
import re
from contextlib import redirect_stdout

f = StringIO()
with redirect_stdout(f): n2medium_request = nb2medium(title = '`+nbTitle+`',
notebook = './`+nbName+`',
log_level = '`+logLevel+`',
log_to_stdout = True)
out = f.getvalue()
urls = re.findall("(https://.*)\\n", out)
for url in urls:
    out = re.sub(re.escape(url), f"<a target='_blank' href='{url}'>{url}</a>", out)
print(re.sub('\\n', '<br />', out))
`)
   }
    
   var nb2mediumRun = function() {
        articleSubmitDialog();
    };
    
    
    function nb2mediumButton() {

        var action = {
            icon: 'fa-medium', // a font-awesome class used on buttons, etc
            help    : 'Upload notebook to Medium',
            handler : nb2mediumRun
        };
        var prefix = 'nb2medium';
        var action_name = 'upload-notebook-to-medium';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); 
        Jupyter.toolbar.add_buttons_group([full_action_name]);

    }
    
    async function nb2mediumSaveAndUpload () {
        await Jupyter.notebook.save_notebook();
        nb2mediumRun();
    };
    
    var nb2medium_menu = function () {
        if ($('#nb2medium_menu').length === 0) {

            var nb2mediumMenu = $('<a/>').attr('href', '#')
                .addClass('dropdown-toogle')
                .attr('data-toggle', 'dropdown')
                .attr('aria-expanded', 'false')
                .text('nb2medium')
                .attr('title', 'Upload Jupyter notebook to Medium');
            
            var nb2mediumActions = $('<ul/>')
                .attr('id', 'nb2medium_actions')
                .addClass("dropdown-menu");
            
            // nb2medium_faq
            var nb2medium_guide = $('<li/>').append($('<a/>')
                .text('nb2medium README')
                .attr('title', "Getting started guide. Opens in a new window.")
                .on('click', function () {
                    window.open('https://github.com/lc5415/nb2medium#nb2medium')
                })
                .prepend($('<i/>').addClass('pull-right'))
            );
            
            var nb2medium_upload = $('<li/>').append($('<a/>')
                .text('Upload to Medium')
                .attr('title', "Upload notebook to Medium")
                .on('click', nb2mediumRun)                                  
                .prepend($('<i/>').addClass("fa fa-upload menu-icon pull-right"))
            );
            
            var nb2medium_save_and_upload = $('<li/>').append($('<a/>')
                .text('Save and upload to Medium')
                .attr('title', "Saves notebook and uploads it to Medium")
                .on('click', nb2mediumSaveAndUpload )
                .prepend($('<i/>').addClass("fa menu-icon pull-right"))
            );
            
            // Jupytext menu
            $('#open_notebook').before('<li id="nb2medium_sub_menu"/>');
            $('#nb2medium_sub_menu').addClass('dropdown-submenu').append(nb2mediumMenu).append(nb2mediumActions);
            nb2mediumActions.append(nb2medium_guide);
            nb2mediumActions.append($('<li/>').addClass('divider'));
            nb2mediumActions.append(nb2medium_upload);
            nb2mediumActions.append(nb2medium_save_and_upload);

        }
    };

    var load_ipython_extension = function () {
        // Wait for the notebook to be fully loaded
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            // this tests if the notebook is fully loaded
            console.log("[nb2medium] Notebook fully loaded -- nb2medium extension initialized ");
            nb2medium_menu();
            // nb2medium button
            nb2mediumButton();
        } else {
            console.log("[nb2medium] Waiting for notebook availability");
            events.on("notebook_loaded.Notebook", function () {
                console.log("[nb2medium] nb2medium initialized (via notebook_loaded)");
                nb2medium_menu();
                // nb2medium button
                nb2mediumButton();
            })
        }     
        
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});
