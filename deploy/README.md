# Updating Deployed Application

**NOTE**: This is specific to deploying the Solara-based application *only*.

1. Create a zipped source file. Only the files in this directory need to be included. Due to quirks of using your OS's built-in compression functions, it's advised to use the following command:
    ```
    $ cd /path/to/hubbleds/deploy
    $ zip ../cds-hubble.zip -r * .[^.]*
    ```
   The `cds-hubble.zip` file will be created in the top-level directory. Note that it is necessary to zip the files directly; i.e. do not zip the `deploy` directory.
2. Log into the AWS console and navigation to `Elastic Beanstalk`. In the `Environments` list, select `cdshubble-env`.
3. In the upper-right corner click the button `Upload and Deploy`, click `Choose file` and select the `cds-hubble.zip`. Pick a new version label. Previous uploaded versions can be seen in the `Application versions` section of the AWS console.
4. Click `Deploy`, and wait for the deployment to finish.
5. Celebrate!