# Data Validator

Implementation of a data validator in Python. Supports two expectations of the data, namely "expect values" and "expect
range". This is a simplified version of the `Great Expressions` Python module.

To execute the program, navigate to the ```data_validator``` directory and run ```data_validator.py```.

    usage: data_validator.py [-h] --data_file DATA_FILE --result_file RESULT_FILE --config_file CONFIG_FILE

    Validate data based on configuration
    
    options:
      -h, --help            show this help message and exit
      --data_file DATA_FILE
                            Path to the input data file (CSV)
      --result_file RESULT_FILE
                            Path to the validation results file
      --config_file CONFIG_FILE
                            Path to the configuration file (YAML or JSON)

# Usage

## PyYAML

The PyYAML module is required to run the program. This can be installed by running the command ```pip install PyYAML``` or ```pip install -r requirements.txt```.

## Input CSV File

A CSV file is required as input whose contents are to be validated. Currently, only the pipe character delimiter ```|``` is supported.

## Configuration File

A configuration file (YAML or JSON) is required that specifies the single expectation suite and the collection of expectations within that suite. For example, the contents of a YAML configuration file ```expectations.yml``` looks like
this:

```yaml
suite:
  name: myexpectations
  expectations:
    first_exp_code:
      expect_values:
        fld_name: warranty_duration
        values:
          - A
          - B
          - C
    second_exp_code:
      expect_range:
        fld_name: amount
        range_lwr: 1
        range_upr: 10
```

The contents of a JSON configurations file `expectations.json` looks like this:

```json
{
  "suite": {
    "name": "myexpectations",
    "expectations": {
      "first_exp_code": {
        "expect_values": {
          "fld_name": "warranty_duration",
          "values": [
            "A",
            "B",
            "C"
          ]
        }
      },
      "second_exp_code": {
        "expect_range": {
          "fld_name": "amount",
          "range_lwr": 1,
          "range_upr": 10
        }
      }
    }
  }
}
```
