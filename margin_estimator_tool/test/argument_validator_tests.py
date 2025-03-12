import pytest
import click
from unittest.mock import patch


from margin_estimator_tool.src.margin_estimator_tool.core.argument_validator import (BaseArgumentValidator,
                                                                                     MarginCalculatorValidator,
                                                                                     GetProductsValidator,
                                                                                     GetSeriesValidator,
                                                                                     GetLiveSnapshotsValidator,
                                                                                     GetSnapshotsValidator,
                                                                                     EtdPortfolioValidator)


class TestBaseArgumentValidator:
    def test_validate_date_valid(self):
        """Test that valid date passes validation"""
        try:
            BaseArgumentValidator.validate_date("20250101")
        except click.BadParameter:
            pytest.fail("validate_date raised BadParameter unexpectedly for valid date")

    def test_validate_date_invalid(self):
        """Test that invalid date raises BadParameter"""
        with pytest.raises(click.BadParameter) as excinfo:
            BaseArgumentValidator.validate_date("2025-01-01")
        assert "Date format must be YYYYMMDD" in str(excinfo.value)

        with pytest.raises(click.BadParameter):
            BaseArgumentValidator.validate_date("20251301")  # Invalid month

    def test_validate_dir_exists(self):
        """Test that existing directory passes validation"""
        with patch('os.path.exists', return_value=True):
            try:
                BaseArgumentValidator.validate_dir("/existing/dir")
            except click.BadParameter:
                pytest.fail("validate_dir raised BadParameter unexpectedly for existing directory")

    def test_validate_dir_not_exists(self):
        """Test that non-existing directory raises BadParameter"""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(click.BadParameter) as excinfo:
                BaseArgumentValidator.validate_dir("/nonexistent/dir")
            assert "Directory '/nonexistent/dir' not found" in str(excinfo.value)

    def test_validate_not_implemented(self):
        """Test that base validate method raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            BaseArgumentValidator().validate()


class TestMarginCalculatorValidator:
    def setup_method(self):
        self.validator = MarginCalculatorValidator()

    def test_validate_all_valid(self):
        """Test validation with all valid parameters"""
        with patch('os.path.exists', return_value=True):
            try:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date_from="20250101",
                    date_to="20250131",
                    export_dir="/path/to/export"
                )
            except click.BadParameter:
                pytest.fail("Validation failed with valid parameters")

    def test_validate_invalid_csv_file(self):
        """Test validation with non-existing csv file"""
        with patch('os.path.exists', side_effect=[False, True]):  # csv_file not exists, export_dir exists
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/nonexistent/file.csv",
                    date_from="20250101",
                    date_to="20250131",
                    export_dir="/path/to/export"
                )
            assert "not found" in str(excinfo.value)

    def test_validate_invalid_date_from(self):
        """Test validation with invalid date_from"""
        with patch('os.path.exists', return_value=True):
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date_from="invalid",
                    date_to="20250131",
                    export_dir="/path/to/export"
                )
            assert "Date format" in str(excinfo.value)

    def test_validate_invalid_date_to(self):
        """Test validation with invalid date_to"""
        with patch('os.path.exists', return_value=True):
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date_from="20250101",
                    date_to="invalid",
                    export_dir="/path/to/export"
                )
            assert "Date format" in str(excinfo.value)

    def test_validate_invalid_export_dir(self):
        """Test validation with non-existing export directory"""
        with patch('os.path.exists', side_effect=[True, False]):  # csv_file exists, export_dir not exists
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date_from="20250101",
                    date_to="20250131",
                    export_dir="/nonexistent/export"
                )
            assert "not found" in str(excinfo.value)


class TestGetProductsValidator:
    def setup_method(self):
        self.validator = GetProductsValidator()

    def test_validate_all_valid(self):
        """Test validation with all valid parameters"""
        with patch('os.path.exists', return_value=True):
            try:
                self.validator.validate(
                    date="20250101",
                    export_dir="/path/to/export"
                )
            except click.BadParameter:
                pytest.fail("Validation failed with valid parameters")

    def test_validate_none_parameters(self):
        """Test validation with None parameters which are optional"""
        try:
            self.validator.validate(
                date=None,
                export_dir=None
            )
        except Exception:
            pytest.fail("Validation failed with None parameters")

    def test_validate_invalid_date(self):
        """Test validation with invalid date"""
        with pytest.raises(click.BadParameter) as excinfo:
            self.validator.validate(
                date="invalid",
                export_dir=None
            )
        assert "Date format" in str(excinfo.value)

    def test_validate_invalid_export_dir(self):
        """Test validation with non-existing export directory"""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    date=None,
                    export_dir="/nonexistent/export"
                )
            assert "not found" in str(excinfo.value)


class TestGetSeriesValidator:
    def setup_method(self):
        self.validator = GetSeriesValidator()

    def test_validate_all_valid(self):
        """Test validation with all valid parameters"""
        with patch('os.path.exists', return_value=True):
            try:
                self.validator.validate(
                    date="20240101",
                    export_dir="/path/to/export"
                )
            except click.BadParameter:
                pytest.fail("Validation failed with valid parameters")

    def test_validate_none_parameters(self):
        """Test validation with None parameters which are optional"""
        try:
            self.validator.validate(
                date=None,
                export_dir=None
            )
        except Exception:
            pytest.fail("Validation failed with None parameters")

    def test_validate_invalid_date(self):
        """Test validation with invalid date"""
        with pytest.raises(click.BadParameter) as excinfo:
            self.validator.validate(
                date="invalid",
                export_dir=None
            )
        assert "Date format" in str(excinfo.value)

    def test_validate_invalid_export_dir(self):
        """Test validation with non-existing export directory"""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    date=None,
                    export_dir="/nonexistent/export"
                )
            assert "not found" in str(excinfo.value)


class TestGetLiveSnapshotsValidator:
    def setup_method(self):
        self.validator = GetLiveSnapshotsValidator()

    def test_validate_valid_date(self):
        """Test validation with valid date"""
        try:
            self.validator.validate(date="20250101")
        except click.BadParameter:
            pytest.fail("Validation failed with valid date")

    def test_validate_invalid_date(self):
        """Test validation with invalid date"""
        with pytest.raises(click.BadParameter) as excinfo:
            self.validator.validate(date="invalid")
        assert "Date format" in str(excinfo.value)


class TestGetSnapshotsValidator:
    def setup_method(self):
        self.validator = GetSnapshotsValidator()

    def test_validate_all_valid(self):
        """Test validation with all valid parameters"""
        try:
            self.validator.validate(
                date_from="20250101",
                date_to="20250131"
            )
        except click.BadParameter:
            pytest.fail("Validation failed with valid parameters")

    def test_validate_none_parameters(self):
        """Test validation with None parameters which are optional"""
        try:
            self.validator.validate(
                date_from=None,
                date_to=None
            )
        except Exception:
            pytest.fail("Validation failed with None parameters")

    def test_validate_invalid_date_from(self):
        """Test validation with invalid date_from"""
        with pytest.raises(click.BadParameter) as excinfo:
            self.validator.validate(
                date_from="invalid",
                date_to="20250131"
            )
        assert "Date format" in str(excinfo.value)

    def test_validate_invalid_date_to(self):
        """Test validation with invalid date_to"""
        with pytest.raises(click.BadParameter) as excinfo:
            self.validator.validate(
                date_from="20250101",
                date_to="invalid"
            )
        assert "Date format" in str(excinfo.value)


class TestEtdPortfolioValidator:
    def setup_method(self):
        self.validator = EtdPortfolioValidator()

    def test_validate_all_valid(self):
        """Test validation with all valid parameters"""
        with patch('os.path.exists', return_value=True):
            try:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date="20250101",
                    export_dir="/path/to/export"
                )
            except click.BadParameter:
                pytest.fail("Validation failed with valid parameters")

    def test_validate_only_required_valid(self):
        """Test validation with only required parameter valid"""
        with patch('os.path.exists', return_value=True):
            try:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date=None,
                    export_dir=None
                )
            except click.BadParameter:
                pytest.fail("Validation failed with only required parameter")

    def test_validate_invalid_csv_file(self):
        """Test validation with non-existing csv file"""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/nonexistent/file.csv",
                    date=None,
                    export_dir=None
                )
            assert "not found" in str(excinfo.value)

    def test_validate_invalid_date(self):
        """Test validation with invalid date"""
        with patch('os.path.exists', return_value=True):
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date="invalid",
                    export_dir=None
                )
            assert "Date format" in str(excinfo.value)

    def test_validate_invalid_export_dir(self):
        """Test validation with non-existing export directory"""
        with patch('os.path.exists', side_effect=[True, False]):  # csv_file exists, export_dir not exists
            with pytest.raises(click.BadParameter) as excinfo:
                self.validator.validate(
                    csv_file="/path/to/file.csv",
                    date=None,
                    export_dir="/nonexistent/export"
                )
            assert "not found" in str(excinfo.value)