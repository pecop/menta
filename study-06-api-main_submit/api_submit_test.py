import api_submit

def test_main():
    output_df = api_submit.main()
    assert len(output_df) == 30

test_main()