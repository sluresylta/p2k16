from p2k16 import P2k16UserException
from p2k16.models import User, Group, GroupMember
from p2k16.database import db


def users_in_group(group_id):
    return User.query. \
        join(GroupMember, GroupMember.user_id == User.id). \
        filter(GroupMember.group_id == group_id). \
        all()


def is_user_in_group(group_id, user_id):
    q = User.query. \
        join(GroupMember, GroupMember.user_id == User.id). \
        filter(GroupMember.group_id == group_id). \
        filter(User.id == user_id)
    return db.session.query(db.literal(True)).filter(q.exists()).scalar()


def add_user_to_group(user_id, group_id, admin_id):
    user = User.find_user_by_id(user_id)
    admin = User.find_user_by_id(admin_id)
    group = Group.find_by_id(group_id)

    if user is None or admin is None or group is None:
        raise P2k16UserException('Bad values')

    group_admin = Group.find_by_name(group.name + '-admin')

    if group_admin is None:
        raise P2k16UserException('No admin-group for group "%s"' % group.name)

    if not is_user_in_group(group_admin.id, admin_id):
        raise P2k16UserException('User %s is not an administrator of %s' % (admin.username, group.description))

    db.session.add(GroupMember(group, user, admin))