from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterUser(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_want_to_find = State()
    waiting_age = State()
    waiting_university = State()
    waiting_faculty = State()
    waiting_photo = State()
    waiting_about = State()


class VerUser(StatesGroup):
    not_verified = State()
    is_verified = State()


class ProfileViewer(StatesGroup):
    waiting_profile = State()
    waiting_response = State()


class Complaint(StatesGroup):
    waiting_message = State()
    complaint_user = ''


class BanUser(StatesGroup):
    user_to_ban_id = 0
    waiting_comment = State()


class LoveLetter(StatesGroup):
    letter_photo = ''
    waiting_for_decision = State()
    waiting_for_letter = State()
    waiting_for_category = State()
    waiting_for_approvement = State()


class DeactivateProfile(StatesGroup):
    waiting_for_approvement = State()


class AdminMassPost(StatesGroup):
    post_photo = ''
    waiting_for_post = State()
    waiting_for_approvement = State()
