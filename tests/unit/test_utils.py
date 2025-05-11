from src.utils import elevaQuadado, requires_role
from unittest.mock import Mock, patch
import pytest

from http import HTTPStatus

@pytest.mark.parametrize("test_input, expected", [(2,4),(10,100), (3,9)])
def test_elevaQuadradoSucesso(test_input, expected):
    resultado = elevaQuadado(test_input)
    assert resultado == expected

@pytest.mark.parametrize(
    "test_input, exc_class,msg",
    [
        ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int' "),
        (None, TypeError, "unsupported operand type(s) for ** or pow (): 'NoneType' and 'int' "),
    ],
)

def test_eleva_quadrado_falha(test_input, exc_class, msg):
    with pytest.raises(exc_class)as exc:
        elevaQuadado(test_input)
        assert str(exc.value) == msg



def test_requires_role():
    mock_user = Mock()
    mock_user.role.name = "admin"

    mock_get_jwt_identity = patch('src.utils.get_jwt_identity')
    mock_db_get_or_404 = patch('src.utils.db.get_or_404', return_value=mock_user)
    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorate_function = requires_role('admin')(lambda: "success")
    result = decorate_function()

    assert result == "success"
    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()
