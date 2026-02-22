FROM ruby:3.3

RUN apt-get update && apt-get install -y \
    libmagickwand-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Gemfile honeybii.gemspec ./
RUN bundle install

COPY . .

ENTRYPOINT ["bundle", "exec"]
CMD ["ruby", "bin/honeybii"]
