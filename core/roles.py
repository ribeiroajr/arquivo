from rolepermissions.roles import AbstractUserRole

class Sin(AbstractUserRole):
    available_permissions = {
        'criar': True,
        'editar': True,
        'excluir': True,
        'gerar': True,
        'import': True,
        'lista': True,
        'cadastro_user': True,
        'reset_user': True,
    }

class Dpl_admin(AbstractUserRole):
    available_permissions = {
        'criar': True,
        'editar': True,
        'excluir': True,
        'gerar': True,
        'import': True,
        'lista': True,
        'reset_user': True,
    }

class Dpl(AbstractUserRole):
    available_permissions = {
        'criar': True,
        'editar': True,
        'gerar': True,
        'import': True,
        'lista': True,
    }

class Div(AbstractUserRole):
    available_permissions = {
        'lista': True,
    }
