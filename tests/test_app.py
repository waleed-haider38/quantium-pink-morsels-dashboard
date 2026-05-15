from app import app


def find_component_by_id(component, target_id):
    if getattr(component, "id", None) == target_id:
        return component

    children = getattr(component, "children", None)

    if children is None:
        return None

    if not isinstance(children, list):
        children = [children]

    for child in children:
        result = find_component_by_id(child, target_id)
        if result is not None:
            return result

    return None


def test_header_is_present():
    header = find_component_by_id(app.layout, "app-header")

    assert header is not None
    assert "Soul Foods Pink Morsels Sales Visualiser" in header.children


def test_visualisation_is_present():
    chart = find_component_by_id(app.layout, "sales-chart")

    assert chart is not None


def test_region_picker_is_present():
    region_picker = find_component_by_id(app.layout, "region-filter")

    assert region_picker is not None