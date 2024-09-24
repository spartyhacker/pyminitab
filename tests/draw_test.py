import pyminitab
import numpy as np
import pandas as pd
import pytest


def test_box():
    data = np.random.normal(loc=0.546, scale=0.019, size=100)
    fig = pyminitab.box(data, USL=1, LSL=0.4)
    assert all(fig.get_size_inches() == [7, 5])
    fig.savefig("test.png")


def test_box_category_unequal_data():
    xl_data = pd.read_excel(r"tests\data.xlsx")
    cat = xl_data["cat"].iloc[:5]
    val = xl_data["val"].iloc[:9]
    with pytest.raises(AssertionError) as excinfo:
        fig = pyminitab.box(val, cat)
    assert str(excinfo.value) == "category and data not equal in length"


def test_box_category():
    xl_data = pd.read_excel(r"tests\data.xlsx")
    cat = xl_data["cat"]
    val = xl_data["val"]
    fig = pyminitab.box(val, cat, LSL=0, USL=200, title="Test Plot")
    fig.savefig("test_output/cat_box.png")
    assert all(fig.get_size_inches() == [7, 5])


def main():
    test_box()


if __name__ == "__main__":
    main()
