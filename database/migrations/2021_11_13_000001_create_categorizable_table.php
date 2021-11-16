<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateCategorizableTable extends Migration
{
    private const TABLE_NAME = 'categorizables';

    /**
     * Run the migrations.
     *
     * @return void
     * @throws Exception
     */
    public function up()
    {
        $shouldCreateCategorizableTable = $this->checkIfNeedToCreateCategorizableTable();

        if ($shouldCreateCategorizableTable && !Schema::hasTable(self::TABLE_NAME)) {
            $this->createTable();
        } elseif (!$shouldCreateCategorizableTable) {
            $this->dropTableIfExists();
        }
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     * @throws Exception
     */
    public function down()
    {
        $this->dropTableIfExists();
    }

    private function checkIfNeedToCreateCategorizableTable(): bool
    {
        return get_models()->some(function ($value) {
            return is_model_using_categories_trait($value);
        });
    }

    private function createTable()
    {
        Schema::create(self::TABLE_NAME, function (Blueprint $table) {
            $table->id();
            $table->foreignId('category_id')
                ->references('id')
                ->on('categories')
                ->cascadeOnDelete();
            $table->integer('categorizable_id');
            $table->string('categorizable_type');
            $table->timestamps();
        });
    }

    private function dropTableIfExists()
    {
        Schema::dropIfExists(self::TABLE_NAME);
    }
}
