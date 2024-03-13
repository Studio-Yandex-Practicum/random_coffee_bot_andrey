@default_router.message(Command('name'))
async def command_name(message: Message, state: FSMContext):
    """Ввод команды /name"""
    await message.answer('Введите свои имя и фамилию')
    await state.set_state(Register.get_name)


@default_router.message(Register.get_name)
async def get_name(message: Message, state: FSMContext):
    """Получение имени и фамилии"""
    full_name = await get_entered_name(message.text)

    if not full_name:
        await message.answer('Введите, свои имя и фамилию, состоящие только '
                             'из букв и разделенные пробелом.')
        return

    await message.answer('Теперь введите свой e-mail')
    await state.update_data(full_name=full_name)
    await state.set_state(Register.get_email)


@default_router.message(Register.get_email)
async def get_email(message: Message, state: FSMContext):
    """ Получение почты """
    email = message.text.lower()
    pattern = rf'^[a-zA-Z0-9._]+' \
              rf'{re.escape(ALLOWED_DOMAIN)}\.' \
              rf'[a-zA-Z0-9._]'
    if not re.match(pattern, email):
        await message.answer(
            'Кажется, что указана не та почта, '
            'пожалуйста, для регистрации укажите именно рабочую почту'
        )
    else:
        context_data = await state.get_data()
        full_name = context_data.get('full_name')
        await create_tg_user(
            user=message.from_user,
            email=email,
            enter_full_name=full_name
        )
        await message.answer(
            'Пользователь зарегистрирован.')
        # await state.clear()


@default_router.message(Command('user'))
async def get_user_id(message: Message, state: FSMContext):
    await message.answer("Введите ID пользователя:")
    await state.set_state(Register.get_user)


@default_router.message(Register.get_user)
async def get_user_data(message: Message, state: FSMContext):
    user_id = int(message.text)
    user = await get_tg_user(user_id)
    if user:
        await message.answer(
            f"Информация о пользователе:\nID: {user.id}\nИмя: {user.enter_full_name}\nEmail: {user.email}")
    else:
        await message.answer("Пользователь с таким ID не найден.")
    await state.clear()