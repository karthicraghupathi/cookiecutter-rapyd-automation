def test_bake_project(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "Python Boilerplate",
            "project_slug": "python_boilerplate",
            "project_description": "Python Boilerplate contains all the\
                 boilerplate you need to create a Python package.",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "python_boilerplate"
    assert result.project_path.is_dir()
