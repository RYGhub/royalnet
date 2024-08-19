use std::hash::{Hash, Hasher};

use anyhow::Context;
use chrono::Datelike;
use rand::SeedableRng;
use rand::seq::SliceRandom;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::prelude::{Message, Requester};
use teloxide::types::ReplyParameters;

use crate::services::telegram::commands::CommandResult;

// Tutte le fortune devono essere positive, o almeno neutrali, per poter essere aggiunte.
const FORTUNES: [&str; 164] = [
	"😄 Oggi sarà una fantastica giornata!",
	"😌 Oggi sarà una giornata molto chill e rilassante.",
	"💰 Oggi sui tuoi alberi cresceranno più Stelline!",
	"🍎 Oggi un unicorno ti lascerà la sua Blessed Apple!",
	"📈 Oggi il tuo team in ranked sarà più amichevole e competente del solito!",
	"🏝 Oggi potrai raggiungere l'Isola Miraggio!",
	"🐱 Oggi vedrai più gatti del solito su Internet!",
	"🐶 Oggi vedrai più cani del solito su Internet!",
	"🐦 Oggi vedrai più uccelli del solito su Internet!",
	"🐌 Oggi incontrerai una chiocciola sperduta!",
	"🎁 Oggi i dispenser di regali in centro funzioneranno senza problemi!",
	"🥕 Oggi il tuo raccolto avrà qualità Iridium Star!",
	"🔴 Oggi troverai più oggetti di rarità rossa del solito!",
	"✨ Oggi farai molti più multicast!",
	"♦️ Oggi troverai una Leggendaria Dorata!",
	"⭐️ Oggi la stella della RYG ti sembrerà un pochino più dritta!",
	"⭐️ Oggi la stella della RYG ti sembrerà anche più storta del solito!",
	"💎 Oggi i tuoi avversari non riusciranno a deflettere i tuoi Emerald Splash!",
	"⬅️ Oggi le tue supercazzole prematureranno un po' più a sinistra!",
	"➡️ Oggi le tue supercazzole prematureranno un po' più a destra!",
	"🌅 Oggi sarà il giorno dopo ieri e il giorno prima di domani!",
	"🤖 Oggi il Royal Bot ti dirà qualcosa di molto utile!",
	"🏠 Oggi qualcuno si autoinviterà a casa tua!",
	"📵 Oggi passerai una bella giornata tranquilla senza che nessuno ti chiami!",
	"🕸 Oggi cadrai trappola di una ragnatela! O ti arriverà in faccia.",
	"🔮 Oggi chiederai a @royalgamesbot di dirti la tua /fortune!",
	"👽 Oggi incontrerai gli UFI!!!1!!uno!",
	"🦾 Oggi uno scienziato pazzo ti proporrà di sostituire il tuo braccio con un braccio-razzo meccanico!",
	"🕵️ Oggi una spia in incognito ti chiederà se hai mai visto the Emoji Movie!",
	"🍕 Oggi mangerai una margherita doppio pomodoro!",
	"🍰 Oggi mangerai una torta al gusto di torta!",
	"🥇 Oggi vincerai qualcosa!",
	"🏴‍☠️ Oggi salperai i sette mari con la tua ciurma pirata!",
	"🕒 Oggi sarà ieri, e domani sarà oggi!",
	"🔙 Oggi tornerai indietro nel tempo!",
	"🚨 Oggi suonerà l'allarme della Velvet Room!",
	"🏳️‍🌈 Oggi scoprirai l'esistenza di almeno un gender che non conoscevi!",
	"🥴 Oggi ti dimenticherai come ci si siede!",
	"👀 Oggi scoprirai di avere degli occhi!",
	"🏹 Oggi ti verrà voglia di installare Arch Linux, ma cambierai idea molto in fretta!",
	"🩲 Oggi annuncerai alla cv di essere in mutande!",
	"👟 Oggi tua madre ti regalerà delle scarpe da corsa!",
	"✨ Oggi troverai un Pokémon shiny!",
	"👏 Oggi sarai felice, lo saprai e batterai le mani!",
	"🦴 Oggi scoprirai di avere uno scheletro wholesome all'interno di te!",
	"💳 Oggi riuscirai a fornire i tre numerini della tua carta di credito a John Wick!",
	"🤔 Oggi smetterai finalmente di essere sus, in quanto sarai confermato dal villaggio!",
	"🔮 Oggi pondererai intensamente la tua sfera!",
	"🗳️ Oggi ci saranno le elezioni per un nuovo partito sul tuo pianeta!",
	"🥓 Oggi avrai bacon illimitato e niente videogiochi!",
	"🎮 Oggi avrai videogiochi, videogiochi illimitati e niente videogiochi!",
	"🔫 Oggi troverai una pistola pearlescent!",
	"🤖 Oggi ti chiederanno di pilotare un robot gigante!",
	"💣 Oggi dovrai continuare a parlare, o esploderai!",
	"🤌 Oggi ti sentirai particolarmente italiano, e gesticolerai più del solito!",
	"🪵 Oggi ti servirà legname!",
	"☄️ Oggi avvisterai una cometa, rischiando di inciampare!",
	"🥅 Oggi farai goal!",
	"🧿 Oggi sarai protetto dagli spiriti maligni che attraversano le pareti!",
	"💰 Oggi è una buona giornata per il capitalismo!",
	"⚒️ Oggi è una buona giornata per il comunismo!",
	"🐰 Oggi inizia la stagione di caccia dei Big Chungus!",
	"🐸 Oggi incontrerai una rana-cavaliere!",
	"⚔️ Oggi un cyborg-samurai ti cederà la sua katana RGB!",
	"🥪 Oggi mangerai un sandvich!",
	"👻 Oggi farai amicizia con Re Boo!",
	"🫀 Oggi un necromante ti ruberà il cuore, e lo farà battere a ritmo!",
	"🦊 Oggi volerai su un Arwing in compagnia di un rinomato mercenario!",
	"🦋 Oggi una tua particolare azione avrà conseguenze, ma potrai tornare indietro nel tempo e correggerla!",
	"🐳 Oggi una balena trasporterà un container per te!",
	"🔥 Oggi sarà una giornata di fuoco!",
	"🥕 Oggi sostituirai il naso a un pupazzo di neve!",
	"🍔 Oggi mangerai il tuo cibo preferito: il sushi!",
	"🍭 Oggi un lecca-lecca ti sbloccherà poteri inimmaginabili!",
	"🧩 Oggi andrai a caccia di Jiggy!",
	"🚜 Oggi piraterai un trattore!",
	"🧭 Oggi ti perderai nei Lost Woods!",
	"⚙️ Oggi aumenterai la produzione di Iron Gear!",
	"🔫 Oggi attiverai il tuo Devil Trigger!",
	"🍺 Oggi servirai un drink con più Karmotrine!",
	"🚽 Oggi sperimenterai la leggendaria Terra Toilet!",
	"🚰 Oggi sarai più idratato del solito!",
	"🔑 Oggi troverai la chiave di tutte le porte!",
	"📎 Oggi incontrerai Clippy!",
	"🌪 Oggi un tornado girerà in senso orario!",
	"🍄 Oggi diventerai Super grazie ad un fungo!",
	"👑 Oggi preparerai la colazione per Re Artù!",
	"🍌 Oggi metterai una banana in microonde!",
	"❤️‍🔥 Oggi scapperai dal Tartaro!",
	"♻️ Oggi, riciclando della Silt, troverai un dinosauro!",
	"🏧 Oggi piazzerai un jammer su un bancomat, estraendone i contenuti!",
	"🚼 Oggi ti chiederai il significato di questa emoji!",
	"🤡 Oggi dovrai interrogare il clown di un circo!",
	"👣 Oggi riceverai un marchio che ti proteggerà dai vampiri!",
	"🎊 Oggi dalle Sfere Festa non uscirà nessuna Bob-omba!",
	"🧲 Oggi piazzerai un magnete per attirare colpi di bazooka!",
	"㊗️ Oggi qualcuno ti farà le sue congratulazioni!",
	"⚛️ Oggi sfrutterai appieno l'energia dell'atomo!",
	"🈁 Oggi ti troverai qui!",
	"💮 Oggi i tuoi esami andranno alla perfezione!",
	"☕️ Oggi berrai un espresso d-d-doppio!?",
	"🐝 Oggi farai quello che fanno le api sulle foglie!",
	"🎰 Oggi vincerai il Jackpot di Francoforte 1!",
	"🧱 Oggi rifiuterai un en passant!",
	"🪓 Oggi perderai la tua ascia, ma la riuscirai facilmente a ritrovare, in quanto starà urlando il tuo nome!",
	"🕳 Oggi cadrai in una Trappola!",
	"⛏ Oggi scaverai degli smeraldi!",
	"🩹 Oggi rigenererai tutta la tua vita con un singolo cerotto!",
	"📈 Oggi i tuoi affari andranno alla grande!",
	"📉 Oggi avrai la possibilità di comprare qualche cosa a prezzo scontato!",
	"🅱️ Oggi la seconda lettera dell'alfabeto ti porterà più fortuna del solito!",
	"🧚 Oggi ti chiederai coraggiosamente dove vola la fatina!",
	"⚔️ Oggi ridurrai dei Corpus a fettine!",
	"🕯 Oggi troverai coraggio nella luce della tua torcia!",
	"🎺 Oggi uno scheletro suonerà una trombetta!",
	"🌋 Oggi getterai un anello in un vulcano!",
	"🧶 Oggi comprerai della lana da fare l'uncinetto!",
	"🐰 Oggi un coniglio ti farà girare la sua ruota!",
	"🧛 Oggi scoprirai finalmente come fa il vampiro ancora a sopravvivere!",
	"👽 Oggi sarai scelto come comandante di una squadra per la difesa planetaria!",
	"🐝 Oggi b!",
	"🎸 Oggi le suonerai a qualcuno!",
	"🧬 Oggi la tua specie si evolverà in un altra con delle bocche sulle mani!",
	"🅰️ Oggi premerai un pulsante a metà!",
	"📻 Oggi sarà il tuo turno di usare la Boombox!",
	"🐡 Oggi riaccenderai un faro sottomarino!",
	"🎄 Oggi addobberai un albero!",
	"🪲 Oggi il tuo insetto metallico sconfiggerà i suoi nemici a suon di musica!",
	"🀄️ Oggi vincerai a Mahjong!",
	"🃏 Oggi vincerai a solitario!",
	"🛗 Oggi l'ascensore ti porterà sulla superficie di Auriga!",
	"🦷 Oggi quattro denti dorati verranno messi sulla bilancia a tuo favore!",
	"✨ Oggi riceverai una /fortune mai vista prima!",
	"🐷 Oggi riceverai una chiamata da un maialino!",
	"🎆 Oggi vedrai dei fuochi artificiali!",
	"🗽 Oggi avrai più libertà del solito!",
	"🎳 Oggi tuo cugino ti inviterà a giocare a bowling!",
	"⛎ Oggi romperai la quarta parete!",
	"🛕 Oggi raggiungerai la cima di un Pantheon!",
	"🍽 Oggi la tua fabbrica produrrà più Iron Plate del normale!",
	"🎲 Oggi tirerai iniziativa, e farai 18!",
	"💊 Oggi una pillola ti darà il potere di mangiare fantasmi!",
	"⚡️ Oggi un tuono colpirà un creeper!",
	"🎈 Oggi delle scimmie ti difenderanno da dei palloncini!",
	"⬆️ Oggi salirai di livello!",
	"🍣 Oggi il sashimi avrà un limite ragionevolmente alto!",
	"🖋 Oggi 'a penn' starà 'ngopp u' tavl!",
	"💰 Oggi il tuo username avrà un valore più alto del solito!",
	"☕️ Oggi un uomo entrerà in un caffè! (Splash.)",
	"☕️ Oggi un uomo entrerà in un caffè! (Tlink.)",
	"💥 Oggi la RYG cambierà governo!",
	"🍛 Oggi il carry farà il curry!",
	"❤️ Oggi ti sentirai pieno di DETERMINAZIONE!",
	"🔄 Oggi cambierai provincia!",
	"🎉 Oggi da qualche parte nel mondo sarà festa!",
	"➡️ Oggi, nonostante gli imprevisti, riuscirai a passare dal Via!",
	"🔎 Oggi accuserai il Professor Plum di aver commesso un omicidio in salotto con un candelabro!",
	"🔫 Oggi schiverai un BANG!",
	"🍻 Oggi una birra ti ridarà una vita!",
	"🎶 Oggi Hatsune Miku si nasconderà nella tua Wi-Fi!",
	"🚽 Oggi delle telecamere combatteranno contro dei gabinetti!",
  	"🌟 Oggi verrà scoperta una galassia grande quanto qualcuno della tua famiglia!",
  	"🎶 Oggi Rick non rinuncerà mai a te!",
  	"🏚 Oggi ristrutturerai una villa completando dei minigiochi match-3!",
];

struct FortuneKey {
	today: chrono::NaiveDate,
	author_id: teloxide::types::UserId
}

impl Hash for FortuneKey {
	fn hash<H: Hasher>(&self, state: &mut H) {
		let days: i32 = self.today.num_days_from_ce();
		let id: u64 = self.author_id.0;

		state.write_i32(days);
		state.write_u64(id);
	}
}

pub async fn handler(bot: &Bot, message: &Message) -> CommandResult {
	let today = chrono::Local::now().date_naive();

	let author = message.from.as_ref()
		.context("Non è stato possibile determinare chi ha inviato questo comando.")?;
	let author_id = author.id;

	let key = FortuneKey {today, author_id};

	let mut hasher = std::hash::DefaultHasher::new();
	key.hash(&mut hasher);
	let hash = hasher.finish()
		.to_le_bytes()
		.into_iter()
		.cycle()
		.take(32)
		.collect::<Vec<u8>>()
		.try_into();
	if hash.is_err() {
		anyhow::bail!("Non è stato possibile determinare il tuo oroscopo.");
	}
	let hash = hash.unwrap();

	let mut rng = rand::rngs::SmallRng::from_seed(hash);

	let fortune = FORTUNES.choose(&mut rng)
		.context("Non è stato possibile selezionare il tuo oroscopo.")?;

	let _reply = bot
		.send_message(message.chat.id, fortune.to_string())
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}