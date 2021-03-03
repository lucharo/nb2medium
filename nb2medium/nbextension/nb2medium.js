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
    
    // I believe tje Jupyter JS api stops taking values after the first stderr 
    // stream comes in, even if the python keeps executuing, run python command
    // outputting data, data.content to check this. And unfortunately the logging 
    // output is seen as stderr
    const pythonPromise = function(python) {
        return new Promise((resolve, reject) => {
            var callbacks = {
                iopub: {
                    output: (data) => {resolve(data.content.text)
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
        if (log_mode == 'console') {
            console.log(pythonResult)
        } else if (log_mode == 'UI') {
            dialog.modal({
                title: "Notebook upload report!", 
                body: i18n.msg.sprintf(i18n.msg._('%s'), pythonResult),
                buttons: {
                    'OK': {'class' : 'btn-primary'}
                }
            });
        }          
    }
    
    // say hi from python, test that execPython works
    const res = pythonExecute("print('Hello from Python!')", 'console')
    
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
    
   var py2js = function(log_level, nb_name, nb_title){
       let pycommand = pythonExecute(`
        from nb2medium.upload import nb2medium
from io import StringIO
from contextlib import redirect_stdout
f = StringIO()
with redirect_stdout(f):
    n2medium_request = nb2medium(
        title = 'hi',
        notebook = './test-gist-output-df.ipynb',
        log_level = 'debug',
        log_to_stdout = True)
print(f.getvalue())`, 'UI')
   }
    
   var nb2mediumRun = function() {
        var nb_name = Jupyter.notebook.notebook_name
        var nb_path = Jupyter.notebook.notebook_path
        var nb_title = prompt("What title would you like to give to this article?", "My Great Article")
        dialog.modal({
            title: i18n.msg._('Upload notebook to Medium'),
            body: $('<a/>').attr('href', '#')
                .addClass(':checkbox')
                .attr('data-toggle', 'dropdown')
                .text('How would you like to upload the notebook?')
                .attr('title', 'How would you like to upload the notebook?'),
            buttons: {'Upload notebook to Medium': {
                        'class' : 'btn-primary',
                        'click' : () => py2js('info', nb_name, nb_title)},
                      'Upload in debugging mode': {
                        'class' : 'btn-secondary',
                        'click': () => py2js('debug', nb_name, nb_title)}
            }
        });

    };
    
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
