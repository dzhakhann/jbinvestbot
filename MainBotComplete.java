import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.ReplyKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MainBot extends TelegramLongPollingBot {

    private static final String TOKEN = "8155499355:AAGm42KV9sfLhqNTEu6onJwURcMx5pUY81A";
    private static final String BOT_USERNAME = "jbinvest_bot";

    // Store user language preferences and referrals
    private Map<Long, String> userLanguages = new HashMap<>();
    private Map<Long, Integer> referralCounts = new HashMap<>();

    @Override
    public String getBotUsername() {
        return BOT_USERNAME;
    }

    @Override
    public String getBotToken() {
        return TOKEN;
    }

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            long chatId = update.getMessage().getChatId();
            String messageText = update.getMessage().getText();

            if (messageText.equals("/start")) {
                sendLanguageSelection(chatId, "Пожалуйста, выберите язык / Iltimos, tilni tanlang:");
            } else if (messageText.equals("⚙️ Настройки") || messageText.equals("⚙️ Sozlamalar")) {
                sendLanguageSelection(chatId, "Пожалуйста, выберите язык / Iltimos, tilni tanlang:");
            } else {
                handleMenuSelection(chatId, messageText);
            }
        } else if (update.hasCallbackQuery()) {
            String data = update.getCallbackQuery().getData();
            long chatId = update.getCallbackQuery().getMessage().getChatId();

            if (data.equals("lang_ru")) {
                userLanguages.put(chatId, "ru");
                sendMainMenu(chatId, "Добро пожаловать! Пожалуйста, выберите опцию из меню ниже:");
            } else if (data.equals("lang_uz")) {
                userLanguages.put(chatId, "uz");
                sendMainMenu(chatId, "Xush kelibsiz! Iltimos, quyidagi menyudan variantni tanlang:");
            }
        }
    }

    private void sendLanguageSelection(long chatId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(text);

        InlineKeyboardMarkup inlineKeyboardMarkup = new InlineKeyboardMarkup();
        List<List<InlineKeyboardButton>> buttons = new ArrayList<>();

        InlineKeyboardButton buttonRu = new InlineKeyboardButton("Русский");
        buttonRu.setCallbackData("lang_ru");
        InlineKeyboardButton buttonUz = new InlineKeyboardButton("O'zbek");
        buttonUz.setCallbackData("lang_uz");

        List<InlineKeyboardButton> row = new ArrayList<>();
        row.add(buttonRu);
        row.add(buttonUz);

        buttons.add(row);
        inlineKeyboardMarkup.setKeyboard(buttons);
        message.setReplyMarkup(inlineKeyboardMarkup);

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private void sendMainMenu(long chatId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(text);

        ReplyKeyboardMarkup replyKeyboardMarkup = new ReplyKeyboardMarkup();
        List<KeyboardRow> keyboard = new ArrayList<>();

        String language = userLanguages.getOrDefault(chatId, "ru");
        if (language.equals("ru")) {
            keyboard.add(createKeyboardRow("💼 Кошелек", "👥 Партнеры"));
            keyboard.add(createKeyboardRow("ℹ️ Инфо", "💬 Отзывы"));
            keyboard.add(createKeyboardRow("👨‍💼 Админ", "⚙️ Настройки"));
        } else {
            keyboard.add(createKeyboardRow("💼 Hamyon", "👥 Hamkorlar"));
            keyboard.add(createKeyboardRow("ℹ️ Ma'lumot", "💬 Sharhlar"));
            keyboard.add(createKeyboardRow("👨‍💼 Admin", "⚙️ Sozlamalar"));
        }

        replyKeyboardMarkup.setKeyboard(keyboard);
        message.setReplyMarkup(replyKeyboardMarkup);

        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    private KeyboardRow createKeyboardRow(String... buttons) {
        KeyboardRow row = new KeyboardRow();
        for (String button : buttons) {
            row.add(new KeyboardButton(button));
        }
        return row;
    }

    private void handleMenuSelection(long chatId, String messageText) {
        String language = userLanguages.getOrDefault(chatId, "ru");

        switch (messageText) {
            case "💼 Кошелек":
            case "💼 Hamyon":
                sendWalletInfo(chatId, language);
                break;
            case "👥 Партнеры":
            case "👥 Hamkorlar":
                sendReferralInfo(chatId, language);
                break;
            case "ℹ️ Инфо":
            case "ℹ️ Ma'lumot":
                sendInfo(chatId, language);
                break;
            case "💬 Отзывы":
            case "💬 Sharhlar":
                sendReviews(chatId, language);
                break;
            case "👨‍💼 Админ":
            case "👨‍💼 Admin":
                sendAdminInfo(chatId, language);
                break;
        }
    }

    private void sendWalletInfo(long chatId, String language) {
        String text = language.equals("ru") ? "Ваш баланс: 0 USD" : "Balansingiz: 0 USD";
        sendSimpleMessage(chatId, text);
    }

    private void sendReferralInfo(long chatId, String language) {
        int referrals = referralCounts.getOrDefault(chatId, 0);
        String referralText = language.equals("ru") ? "Ваши рефералы: " + referrals : "Referallar soni: " + referrals;
        sendSimpleMessage(chatId, referralText);
    }

    private void sendInfo(long chatId, String language) {
        String text = language.equals("ru") ?
            "Мы – команда экспертов по инвестициям, готовая помочь вам." :
            "Biz – sarmoya bo'yicha mutaxassislar jamoasi.";
        sendSimpleMessage(chatId, text);
    }

    private void sendReviews(long chatId, String language) {
        String text = language.equals("ru") ?
            "Читайте отзывы наших клиентов:" :
            "Mijozlarimizning sharhlarini o'qing:";
        sendSimpleMessage(chatId, text);
    }

    private void sendAdminInfo(long chatId, String language) {
        String text = language.equals("ru") ?
            "Связаться с администратором:" :
            "Admin bilan bog'lanish:";
        sendSimpleMessage(chatId, text);
    }

    private void sendSimpleMessage(long chatId, String text) {
        SendMessage message = new SendMessage();
        message.setChatId(chatId);
        message.setText(text);
        try {
            execute(message);
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        try {
            TelegramBotsApi botsApi = new TelegramBotsApi(DefaultBotSession.class);
            botsApi.registerBot(new MainBot());
        } catch (TelegramApiException e) {
            e.printStackTrace();
        }
    }
}
