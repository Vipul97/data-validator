import argparse
import csv
import json
import yaml


class ExpectValues:
    def __init__(self, field_name, expected_values):
        self.field_name = field_name
        self.expected_values = expected_values
        self.failed = False

    def validate(self, row):
        field_value = row.get(self.field_name)

        if field_value not in self.expected_values:
            self.failed = True
            return field_value

    def __str__(self):
        return f'Values must belong to this set: {self.expected_values}.'


class ExpectRange:
    def __init__(self, field_name, range_lower, range_upper):
        self.field_name = field_name
        self.range_lower = range_lower
        self.range_upper = range_upper
        self.failed = False

    def validate(self, row):
        field_value = int(row.get(self.field_name))

        if not self.range_lower <= field_value <= self.range_upper:
            self.failed = True
            return field_value

    def __str__(self):
        return f'Values must be greater than or equal to {self.range_lower} and less than or equal to {self.range_upper}.'


class DataValidator:
    def __init__(self, data_file_path, result_file_path, config_file_path):
        self.data_file_path = data_file_path
        self.result_file_path = result_file_path
        self.config_file_path = config_file_path
        self.suite_name = None
        self.expectations = {}

    def load_expectations(self):
        with open(self.config_file_path, 'r') as config_file:
            if self.config_file_path.endswith('.yml'):
                config_data = yaml.load(config_file, Loader=yaml.Loader)
            else:
                config_data = json.load(config_file)

        suite_info = config_data.get('suite', {})
        self.suite_name = suite_info.get('name', 'Unnamed Suite')

        expectation_configs = suite_info.get('expectations', {})
        for exp_code, exp_config in expectation_configs.items():
            exp_type, exp_params = list(exp_config.items())[0]

            if exp_type == 'expect_values':
                self.expectations[exp_code] = ExpectValues(exp_params['fld_name'], exp_params['values'])
            elif exp_type == 'expect_range':
                self.expectations[exp_code] = ExpectRange(exp_params['fld_name'], exp_params['range_lwr'],
                                                          exp_params['range_upr'])

    def validate(self):
        with open(self.data_file_path, 'r') as data_file, open(self.result_file_path, 'w') as result_file:
            reader = csv.DictReader(data_file, delimiter='|')
            total_rows = 0
            validation_results = {}

            for row in reader:
                total_rows += 1
                for exp_code, expectation in self.expectations.items():
                    field_name = expectation.field_name
                    validation_results.setdefault(field_name, {}).setdefault(exp_code, {})

                    unexpected_value = expectation.validate(row)
                    if unexpected_value:
                        validation_results[field_name][exp_code][unexpected_value] = validation_results[field_name][
                                                                                         exp_code].get(unexpected_value,
                                                                                                       0) + 1

            successful_expectations = sum(1 for expectation in self.expectations.values() if not expectation.failed)
            unsuccessful_expectations = sum(1 for expectation in self.expectations.values() if expectation.failed)
            evaluated_expectations = successful_expectations + unsuccessful_expectations

            result_file.write('Overview:\n')
            result_file.write(f'Expectation Suite: {self.suite_name}\n')
            result_file.write(f'Status: {"Failed" if unsuccessful_expectations > 0 else "Succeeded"}\n\n')
            result_file.write('Statistics:\n')
            result_file.write(f'Evaluated Expectations: {evaluated_expectations}\n')
            result_file.write(f'Successful Expectations: {successful_expectations}\n')
            result_file.write(f'Unsuccessful Expectations: {unsuccessful_expectations}\n')
            result_file.write(f'Success Percent: {(successful_expectations / evaluated_expectations) * 100:.2f}%')

            for field_name, exp_config in validation_results.items():
                result_file.write(f'\n\nField Name: {field_name}')

                for exp_code, unexpected_values in exp_config.items():
                    count = sum(unexpected_values.values())
                    percentage = (count / total_rows) * 100
                    result_file.write(f'\nExpectation: {exp_code} - {self.expectations[exp_code]}')
                    result_file.write(f'\nStatus: {"Failed" if unexpected_values else "Succeeded"}')
                    result_file.write(
                        f'\nResult: {count} unexpected values found. {percentage:.2f}% of {total_rows} total rows.')

                    if unexpected_values:
                        for unexpected_value, count in sorted(unexpected_values.items(), key=lambda x: x[1],
                                                              reverse=True):
                            result_file.write(f'\n- Unexpected Value: {unexpected_value}, Count: {count}')


def main(args):
    data_validator = DataValidator(
        data_file_path=args.data_file,
        result_file_path=args.result_file,
        config_file_path=args.config_file
    )

    data_validator.load_expectations()
    data_validator.validate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate data based on configuration')
    parser.add_argument('--data_file', required=True, help='Path to the input data file (CSV)')
    parser.add_argument('--result_file', required=True, help='Path to the validation results file')
    parser.add_argument('--config_file', required=True, help='Path to the configuration file (YAML or JSON)')

    args = parser.parse_args()
    main(args)
