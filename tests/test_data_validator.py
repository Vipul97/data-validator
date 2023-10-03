from data_validator.data_validator import DataValidator


def validate_data(data_file_path, result_file_path, config_file_path):
    data_validator = DataValidator(
        data_file_path=data_file_path,
        result_file_path=result_file_path,
        config_file_path=config_file_path
    )

    data_validator.load_expectations()
    data_validator.validate()


def main():
    # Validation for 'fail' case
    validate_data('fail_input.csv', 'fail_validation_results.txt', 'expectations.yml')

    # Validation for 'pass' case
    validate_data('pass_input.csv', 'pass_validation_results.txt', 'expectations.json')


if __name__ == '__main__':
    main()
