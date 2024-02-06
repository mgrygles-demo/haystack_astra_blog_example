### This folder houses the initial set of sample code for illustrating the basic usages of the [Haystack-AstraDB integration](https://haystack.deepset.ai/integrations/astradb)
##### Background info:  Integration was announced/released on Jan 17, 2024

###### Details of the examples are described in [this DataStax article <link to be updated>](https://www.datastax.com)

## Files
|File name| Description |
|:-------|:-----------|
|haystack_astra_retrieve.py | The example that illustrates the Q&A usage scenario of how to retieve documents from Astra DB using the Haystack pipeline
|haystack_astra_store.py | The example that illustrates how to store documents into Astra DB using the Haystack pipeline
|haystack_astra_utils.py | A utility file that primarily takes care of setting up the environment
|requirements.txt | List out the dependencies for this set of example files
|README.md | This file
<p>

## Steps to run the examples

<p>Ensure that you have the following required dependency packages installed

    pip install -U astra-haystack sentence-transformers

#### (For MacOS - Only if necessary) 
<p><i>Ensure also that you have 'cmake' installed, and if not, one of the ways to install it is to use Homebrew, as follows:

    brew install cmake
</i>

<p>Set the following environment variables - e.g. on MacOS and most Linux shell variants:

    export ASTRA_DB_ID=<Your Astra DB ID>
    export ASTRA_API_ENDPOINT=<Your database API endpoint>
    export ASTRA_DB_KEYSPACE_NAME=<Your database keyspace name>
    export ASTRA_DB_APPLICATION_TOKEN=<Your application token>
    export ASTRA_DB_COLLECTION_NAME=<The database collection name>

    export OPENAI_API_KEY=<Your OpenAI API KEY>


<p>Clone this repo

    git clone https://github.com/mgrygles-demo/haystack_astra_blog_example

<p>Go to the directory

    cd ./haystack_astra_blog_example

<p>First, store the documents into Astra DB by executing the following on the command line:

    python3 haystack_astra_store.py

When you examine the output in the console, you should see that 3 documents have been successfully added:

    ....
    INFO:haystack.core.pipeline.pipeline:Pipeline executed successfully.
    3

<p>Next, retrieve the document from Astra DB by running the following example script, which would be prompting with a question that asks about the number of languages that are spoken in the world today, and you should see the console output as well as the response document coming back in dictionary format, similar to this:

    INFO:__main__:{'answer_builder': {'answers': [GeneratedAnswer(data='There are over 7,000 languages spoken around the world today.', query='How many languages are there in the world today?', documents=[Document(id=cfe93bc1c274908801e6670440bf2bbba54fad792770d57421f85ffa2a4fcc94, content: 'There are over 7,000 languages spoken around the world today.', score: 0.9267925, embedding: vector of size 384)], meta={'model': 'gpt-3.5-turbo-0613', 'index': 0, 'finish_reason': 'stop', 'usage': {'completion_tokens': 14, 'prompt_tokens': 54, 'total_tokens': 68}})]}}
    {'answer_builder': {'answers': [GeneratedAnswer(data='There '
                                                     'are '
                                                     'over '
                                                     '7,000 '
                                                     'languages '
                                                     'spoken '
                                                     'around '
                                                     'the '
                                                     'world '
                                                     'today.',
                                                query='How '
                                                      'many '
                                                      'languages '
                                                      'are '
                                                      'there '
                                                      'in '
                                                      'the '
                                                      'world '
                                                      'today?',
                                                documents=[Document(id=cfe93bc1c274908801e6670440bf2bbba54fad792770d57421f85ffa2a4fcc94, content: 'There are over 7,000 languages spoken around the world today.', score: 0.9267925, embedding: vector of size 384)],
                                                meta={'finish_reason': 'stop',
                                                      'index': 0,
                                                      'model': 'gpt-3.5-turbo-0613',
                                                      'usage': {'completion_tokens': 14,
                                                                'prompt_tokens': 54,
                                                                'total_tokens': 68}})]}}

__Hint__

If you encounter a runtime error, such as an [ImportError](https://docs.python.org/3/library/exceptions.html#ImportError) that indicates an unreachable haystack library, try setting up a [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments), which should then be able to isolate your particular environment from the "base", and eliminate any potential conflict in not being able to locate the library.   Here's a suggestion as to how you can set your venv up in a few steps:

1. Create your venv (in a .venv sub-folder inside your project folder)

        python3 -m <your_project_folder>/.venv
    
2. Activate your venv (bash/zsh)

        cd <your_project_folder>/.venv
        source bin/activate

*Other shell environments have the following usages:*

| Platform | Shell | Command to activate virtual environment |
|:---------|:-----:|:---------------------------------------:|
|POSIX|bash\/zsh|\$ source \<your_venv_dir\>/bin\/activate
|     |fish|\$ source \<your_venv_dir\>\/bin\/activate.fish
|     |csh/tcsh|\$ source \<your_venv_dir\>\/bin\/activate.csh
|     |PowerShell|\$ \<your_venv_dir\>\/bin\/Activate.ps1
||||
|Windows|cmd.exe|C\:\\\> \<your_venv_dir\>\\Scripts\activate.bat|
|       |PowerShell|PS C\:\\\> \<your_venv_dir\>\\Scripts\Activate.ps1|


3. Deactivate your venv on the command-line (**When you are done with your work)

    deactivate

4. Remove your venv (**Caution: Only when you no longer need your work)

    rm -rf \<your_venv_dir\>