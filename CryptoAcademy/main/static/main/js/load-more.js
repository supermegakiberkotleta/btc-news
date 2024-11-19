$(document).ready(function () {
    let currentPage = 1; // Текущая страница
    let isLoading = false; // Флаг, чтобы избежать повторных запросов

    // Обработчик нажатия на кнопку "Показать еще"
    $('#load-more-btn').on('click', function () {
        if (isLoading) return; // Если уже загружаем, ничего не делаем
        isLoading = true; // Устанавливаем флаг

        $('#load-more-btn').text('Загрузка...'); // Меняем текст кнопки на индикатор загрузки

        $.ajax({
            url: `/news/load-more/`,
            method: 'GET',
            data: {
                page: currentPage + 1 // Увеличиваем номер страницы
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Заголовок для проверки AJAX-запроса
            },
            success: function (response) {
                // Если запрос успешен
                if (response.news_html) {
                    $('#latest-blog .row').append(response.news_html); // Добавляем новые элементы
                }

                if (!response.has_more) {
                    // Если больше новостей нет, скрываем кнопку
                    $('#load-more-btn').hide();
                } else {
                    // Если ещё есть новости, увеличиваем номер страницы
                    currentPage++;
                    $('#load-more-btn').text('Показать еще'); // Возвращаем текст кнопки
                }
            },
            error: function (xhr, status, error) {
                console.error('Ошибка:', error); // Логируем ошибку
                $('#load-more-btn').text('Показать еще'); // Возвращаем текст кнопки
            },
            complete: function () {
                isLoading = false; // Снимаем флаг загрузки
            }
        });
    });
});
