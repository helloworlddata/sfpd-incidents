require 'pathname'

START_YEAR = 2003
END_YEAR = 2016 # TK TODO: END_YEAR should be changed to dynamically be THIS year

WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS = WRANGLE_DIR.join('scripts')

DIRS = {
    'fetched' => CORRAL_DIR.join('fetched'),
    'cleaned' =>  CORRAL_DIR.join('cleaned'),
    'published' => Pathname('catalog'),
}

FILES = {
    'fetched' => (START_YEAR..END_YEAR).map{|y| DIRS['fetched'] / "#{y}.csv"},
    'cleaned' => DIRS['cleaned'] / 'sfpd-incidents.csv',
}

PYR_FILES = Hash[[
    2003..2005,
    2006..2008,
    2009..2011,
    2012..2014,
    2015,
    2016].map{ |p|
                suffix = p.is_a?(Range) ? "#{p.first}-through-#{p.last}" : p
                fname = "sfpd-incidents-#{suffix}.csv"
                [p, DIRS['published'] / fname]
        }]



desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        if !p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end


desc "Fetch data from #{START_YEAR} through #{END_YEAR}"
task :fetch do
    FILES['fetched'].each do |fn|
        Rake::Task[fn].invoke()
    end
end

desc "Create clean and compiled datafile"
task :clean do
    Rake::Task[FILES['cleaned']].execute()
end

desc "Publish the data files"
task :publish do
    PYR_FILES.each_pair do |period, destname|
        Rake::Task[destname].execute()
    end
end

desc "Pull newest year data, recompile and republish"
task :refresh do
    # TK TODO: END_YEAR should be changed to dynamically be THIS year
    thisyear = END_YEAR
    Rake::Task[DIRS['fetched'].join("#{thisyear}.csv")].execute()
    Rake::Task[:clean].execute()
    Rake::Task[PYR_FILES[thisyear]].execute()
end


namespace :filings do # doing this just to visually indicate which tasks are file builders
    PYR_FILES.each_pair do |period, destname|
        desc "Publish period #{period} incidents"
        file destname  do
            cmd = ['csvgrep -c datetime',
                    '-r', %Q{'#{Array(period).join('|')}'},
                   FILES['cleaned'],
                   '>', destname].join(' ')
            sh cmd
        end
    end

    file FILES['cleaned'] => FILES['fetched'] do
        sh ['cat', FILES['fetched'].join(' '), '|',
            'python', SCRIPTS / 'clean.py', '-',
            '>', FILES['cleaned']].join(' ')
    end


    FILES['fetched'].each do |fname|
        year = fname.to_s[/\d{4}(?=\.csv)/]
        file fname => :setup do
            sh "python #{SCRIPTS.join('fetch_year.py')} #{year} > #{fname}"
        end
    end
end
