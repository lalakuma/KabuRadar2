from __future__ import annotations


def test_core_packages_import() -> None:
    from kaburadar.data import repository
    from kaburadar.pipeline import analyze, aggregate
    from kaburadar.publishing import github_pages
    from kaburadar.settings import screening
    from kaburadar.strategy import engine, models, rsi

    assert callable(repository.connect_db)
    assert callable(analyze.run)
    assert callable(aggregate.shuukei_toCsv)
    assert callable(github_pages.build_payload)
    assert callable(screening.get_config)
    assert callable(engine.backtst_proc)
    assert models.KabInf is not None
    assert callable(rsi.rsi_tradingview)
