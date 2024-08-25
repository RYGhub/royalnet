use std::ops::Add;

pub fn countable_noun_suffix<T, U>(count: T, singular: &'static str, plural: &'static str)
								   -> &'static str
where
	T: Default + Add<usize, Output=U> + PartialEq<U>,
{
	match count == (T::default() + 1) {
		true => singular,
		false => plural,
	}
}